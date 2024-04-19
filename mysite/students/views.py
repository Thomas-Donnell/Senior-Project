from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max, OuterRef, Subquery
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from teachers.forms import MyClassForm
from teachers.models import FinalGrade, MyClass, EnrolledUser, Discussion, Reply, Quiz, Question, Grade, Alert, StudentQuestion, Module, ModuleQuestion, ModuleSection, ShortAnswer, StudentShortAnswer
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
# Create your views here.
class CustomStudent:
    def __init__(self, student, average):
        self.student = student
        self.average = average

class CustomGrade:
    def __init__(self, module, grades):
        self.module = module
        self.grades = grades

class CustomAnalytics:
    def __init__(self, course, grades, grade_counts=None):
        self.course = course
        self.grades = grades
        self.grade_counts = grade_counts

def search(request):
    courses = []
    enrolled_courses = EnrolledUser.objects.filter(user=request.user)
    for course in enrolled_courses:
        courses.append(course.course)
    
    if request.method == 'POST':
        subject = request.POST.get('subject')
        quizzes = Quiz.objects.filter(course__in=courses, title__contains = subject)
        classes = (MyClass.objects.filter(teacher=request.user, class_name__contains=subject) | 
        MyClass.objects.filter(teacher=request.user, class_descriptor__contains=subject))
        discussions = Discussion.objects.filter(course__in=courses, subject__contains = subject)

    context = {'subject':subject, 'quizzes':quizzes, 'classes':classes, 'discussions':discussions}
    return render(request, "students/search.html", context)

def home(request):
    classes = []
    form = MyClassForm()

    if request.method == 'POST':
        form = MyClassForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user
            course.save()
    enrolled_courses = EnrolledUser.objects.filter(user=request.user)
    for course in enrolled_courses:
        classes.append(course.course)
    context = {'form':form, 'classes': classes}
    return render(request, "students/home.html", context)

def course(request, course_id):
    my_class = MyClass.objects.get(id=course_id)
    alerts = Alert.objects.filter(student=request.user, course=my_class).count()
    if request.method == 'POST':
        enrolled_user_ids = request.POST.getlist('enrolled_users')  # Get a list of selected user IDs
        enrolled_users = User.objects.filter(id__in=enrolled_user_ids)
        for user in enrolled_users:
            EnrolledUser.objects.create(user=user, course=my_class)
    users = User.objects.all()
    context = {'courseId': course_id, 'users': users, 'my_class': my_class, 'alerts':alerts}
    return render(request, "students/course.html", context)

def deleteCourse(request, course_id):
    course = MyClass.objects.get(pk=course_id)
    course.delete()
    return redirect('students:home')
    
class CustomGrade:
    def __init__(self, module, grades):
        self.module = module
        self.grades = grades

def studentView(request, course_id):
    course = MyClass.objects.get(pk=course_id)
    student = request.user
    custom_grades = []
    average = 0
    weighting_factor = 0
    subquery = Grade.objects.filter(
        student=student,
        module=OuterRef('pk')  # Use OuterRef to reference the quiz being considered
    ).values('module')

    modules = Module.objects.filter(
        course=course,
        pk__in=Subquery(subquery)
    )
    for module in modules:
        grades = Grade.objects.filter(module=module, student=student)
        max_grade = Grade.objects.filter(module=module, student=student).order_by('-grade').first()
        average += (max_grade.grade * max_grade.module.weight)
        weighting_factor += max_grade.module.weight
        custom_grades.append(CustomGrade(module, grades))
    if(len(modules) > 0):
        average = round(average / weighting_factor, 2)
    context = {'courseId': course_id, 'grades': custom_grades, 'average': average}
    return render(request, "students/studentview.html", context)

def discussion(request, course_id):
    my_class = MyClass.objects.get(id=course_id)
    messages = Discussion.objects.filter(course=my_class).order_by('-created_at')
    enrolled_users = EnrolledUser.objects.filter(course=my_class)
    alerts = Alert.objects.filter(student=request.user, course=my_class)
    alerts.delete()
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        uploaded_file = request.FILES.get('upload')
        post = Discussion.objects.create(
            course=my_class, 
            author=request.user, 
            subject=subject, 
            message=message,
            file=uploaded_file 
        )
        for user in enrolled_users:
            Alert.objects.create(
                course=my_class,
                student=user.user,
                post= post
            )
        return redirect(reverse('students:discussion', args=[course_id]))
        
    context = {'courseId': course_id, 'my_class': my_class, 'messages': messages}
    return render(request, "students/discussion.html", context)

def post(request, id, course_id):
    post = Discussion.objects.get(pk=id)
    fileName = post.file.name.split("/")[-1]
    replies = Reply.objects.filter(post=post).order_by('-created_at')
    if request.method == 'POST':
        message = request.POST.get('message')
        Reply.objects.create(post=post, author=request.user, message=message)
        return redirect(reverse('students:post', args=[id, course_id]))
    context = {'post':post, 'replies':replies, 'courseId':course_id, 'fileName':fileName}
    return render(request, "students/post.html", context)


def deletePost(request, id, course_id):
    post = Discussion.objects.get(pk=id)
    post.delete()
    return redirect(reverse('students:discussion', args=[course_id]))

def moduleHub(request, course_id):
    my_class = MyClass.objects.get(id=course_id)
    modules = Module.objects.filter(course=my_class).order_by('-created_at')
        
    context = {'courseId': course_id, 'my_class': my_class, 'modules': modules}
    return render(request, "students/modulehub.html", context)

def moduleView(request, id, course_id):
    module = Module.objects.get(pk=id)
    questions = ModuleQuestion.objects.filter(module=module)
    sections = ModuleSection.objects.filter(module=module)
    position = questions.count() + sections.count()
    shortAnswers = ShortAnswer.objects.filter(module=module)
    position = questions.count() + sections.count() + shortAnswers.count()
    all_questions = []
    i = 0
    j = 0
    while i < questions.count() and j < shortAnswers.count():
        if questions[i].position < shortAnswers[j].position:
            all_questions.append({"type":"multi", "question":questions[i]})
            i += 1 
        else:
            all_questions.append({"type":"short", "question": shortAnswers[j]})
            j += 1
    while i < questions.count():
        all_questions.append({"type":"multi", "question":questions[i]})
        i += 1 
    while j < shortAnswers.count():
        all_questions.append({"type":"short", "question": shortAnswers[j]})
        j += 1
    
    attempt = 0 
    try:
        grades = Grade.objects.filter(module=module, student=request.user)
        attempt = len(grades)

    except ObjectDoesNotExist:
        grades = None

    if request.method == 'POST':
        total_questions = questions.count() + shortAnswers.count()
        correct = 0
        for question in shortAnswers:
            answer = request.POST.get(f"{question.id}")
            StudentShortAnswer.objects.create(
                module=module,
                student=request.user,
                question_text=question.question_text,
                answer=answer,
                attempt=attempt + 1,
                pending=True
            )
        for question in questions:
            selected_answer = int(request.POST.get(f"{question.id}"))
            StudentQuestion.objects.create(
                module=module,
                student=request.user,
                module_question=question,
                selected_answer=selected_answer,
                correct_answer=question.correct_answer,
                attempt=attempt + 1
            )
            if selected_answer == question.correct_answer:
                correct += 1
        total = (correct/total_questions) * 100
        pending = True
        if shortAnswers.count() == 0:
            pending = False

        Grade.objects.create(
            grade = total,
            module=module, 
            student=request.user,
            attempt = attempt + 1,
            pending= pending
        )
        return redirect(reverse('students:moduleView', args=[id, course_id]))
    
    context = {"questions":all_questions, "sections":sections, "module":module, "courseId":course_id, "count":range(position)}
    return render(request, "students/moduleview.html", context)

def quizHub(request, course_id):
    my_class = MyClass.objects.get(id=course_id)
    quizes = Quiz.objects.filter(course=my_class).order_by('-created_at')
    if request.method == 'POST':
        title = request.POST.get('title')
        Quiz.objects.create(
            title = title,
            course=my_class, 
            author=request.user
        )
        return redirect(reverse('students:quizHub', args=[course_id]))
        
    context = {'courseId': course_id, 'my_class': my_class, 'quizes': quizes}
    return render(request, "students/quizhub.html", context)

def quiz(request, id, course_id):
    quiz = Quiz.objects.get(pk=id)
    context = {"quiz":quiz, "courseId":course_id}
    return render(request, "students/quiz.html", context)

def quizView(request, id, course_id):
    #Get quiz, questions, and grade model objects
    quiz = Quiz.objects.get(pk=id)
    questions = Question.objects.filter(quiz=quiz)
    attempt = 0 
    try:
        grades = Grade.objects.filter(quiz=quiz, student=request.user)
        attempt = len(grades)
        # Annotate the query with the maximum grade
        grades = grades.annotate(max_grade=Max('grade'))
        # Order the results in descending order by the maximum grade
        highest_grade = grades.order_by('-max_grade').first()
    except ObjectDoesNotExist:
        grades = None
    
    if request.method == 'POST':
        total_questions = len(questions)
        correct = 0
        for question in questions:
            selected_answer = int(request.POST.get(f"{question.id}"))
            StudentQuestion.objects.create(
                quiz=quiz,
                student=request.user,
                question=question,
                selected_answer=selected_answer,
                correct_answer=question.correct_answer,
                attempt=attempt + 1
            )
            if selected_answer == question.correct_answer:
                correct += 1
        total = correct/total_questions * 100
        Grade.objects.create(
            grade = total,
            quiz=quiz, 
            student=request.user,
            attempt = attempt + 1
        )
        return redirect(reverse('students:quizView', args=[id, course_id]))
    
    context = {"questions":questions, "quiz":quiz, "courseId":course_id, "attempt":attempt, "grade":highest_grade}
    return render(request, "students/quizview.html", context)

def settings(request, url):
    context = {"url":url}
    return render(request, "students/settings.html", context)

def changeUsername(request, url):
    if request.method == 'POST':
        new_username = request.POST['new_username']
        user = User.objects.get(username=request.user.username)
        try:
            user.username = new_username
            user.save()
            messages.success(request, 'Username changed successfully.')
        except Exception as e:
            messages.error(request, "This Username is already In use")
            
        return redirect(reverse('students:settings', args=[url]))  # Redirect to the user's profile page or another appropriate page

def changePassword(request, url):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Update the session to prevent logging the user out
            messages.success(request, 'Password changed successfully.')
        else:
            messages.error(request, 'Could Not change password, Please Check length')
            return redirect(reverse('students:settings', args=[url]))  # Redirect to the user's profile page or another appropriate page
        
def studentReport(request):
    selected_student = request.user
    final_grades = FinalGrade.objects.filter(student=selected_student)
    terms = []
    for grade in final_grades:
        if grade.term not in terms:
            terms.append(grade.term)

    courses = MyClass.objects.filter(enrolleduser__user=selected_student)

    subquery = Grade.objects.filter(
        student=OuterRef('student'),
        module=OuterRef('module')
    ).order_by('-grade').values('grade')[:1]

    custom_grades = []

    for course in courses:
        grades = []
        index = 0
        student_grade = 0
        course_students = EnrolledUser.objects.filter(course=course)
        for student in course_students:
            total = 0
            weighting_factor = 0
            grades_highest = Grade.objects.filter(
                student=student.user,
                module__course=course,
                grade=Subquery(subquery)
            )

            if grades_highest.exists():
                for grade in grades_highest:
                    total += (grade.grade * grade.module.weight)
                    weighting_factor += grade.module.weight
                total = round(total / weighting_factor, 2)
            grades.append(CustomStudent(student.user, total))
            grades = sorted(grades, key=lambda x: x.average, reverse=False)
        for grade in grades:
            if grade.student == selected_student:
                student_grade = grade.average
                break
            else:    
                index += 1
        percentile = round((index/len(grades))*100, 2)
        custom_grades.append(CustomAnalytics(course, percentile, student_grade))

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = []
        for grade in custom_grades:
            data.append({
                'course_name': grade.course.class_name,
                'percentile': grade.grades,
                'grades': grade.grade_counts,
            })
        return JsonResponse(data, safe=False)
    context={'terms':terms}
    return render(request, "students/studentreport.html", context)

def pastSemester(request, term):
    student = request.user
    grades = FinalGrade.objects.filter(student=student, term=term)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = []
        for grade in grades:
            data.append({
                'course_name': grade.course_name,
                'percentile': grade.percentile,
                'grades': grade.grade,
            })
        return JsonResponse(data, safe=False)
    
def anime(request):
    context={}
    return render(request, "students/anime_view.html", context)
