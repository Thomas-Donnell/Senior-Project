from decimal import Decimal
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.db.models import Max, Subquery, OuterRef, Avg
from django.urls import reverse
from .forms import MyClassForm
from .models import MyClass, EnrolledUser, Discussion, Reply, Quiz, Question, Grade, Alert, StudentQuestion, FinalGrade, Module, ModuleQuestion, ModuleSection, Prefab, StudentModule, ShortAnswer, StudentShortAnswer
from users.models import Account
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
    students = []
    courses = MyClass.objects.filter(teacher=request.user)
    
    if request.method == 'POST':
        subject = request.POST.get('subject')
        quizzes = Quiz.objects.filter(course__in=courses, title__contains = subject)
        classes = (MyClass.objects.filter(teacher=request.user, class_name__contains=subject) | 
        MyClass.objects.filter(teacher=request.user, class_descriptor__contains=subject))
        discussions = Discussion.objects.filter(course__in=courses, subject__contains = subject)
        student_ids = EnrolledUser.objects.filter(course__in=courses, user__username__contains=subject).values('user').distinct()

        for student in student_ids:
            students.append(User.objects.get(pk=student['user'])) 
    context = {'subject':subject, 'quizzes':quizzes, 'classes':classes, 'discussions':discussions, 'students':students}
    return render(request, "teachers/search.html", context)

def home(request):
    if request.method == 'POST':
        class_name = request.POST.get('class_name')
        descriptor = request.POST.get('descriptor')
        year = request.POST.get('year')
        term = request.POST.get('term')
        semester = f"{term} {year}"
        MyClass.objects.create(
            class_descriptor=descriptor, 
            class_name=class_name, 
            term=semester, 
            teacher=request.user
        )
    classes = MyClass.objects.filter(teacher=request.user)
    context = {'classes': classes}
    return render(request, "teachers/home.html", context)

def course(request, course_id):
    my_class = MyClass.objects.get(id=course_id)
    students = EnrolledUser.objects.filter(course=my_class)
    custom_students = []
    subquery = Grade.objects.filter(
        student=OuterRef('student'),
        module=OuterRef('module')
    ).order_by('-grade').values('grade')[:1]

    for student in students:
        total = 0
        weighting_factor = 0
        grades_highest = Grade.objects.filter(
            student=student.user,
            module__course=my_class,
            grade=Subquery(subquery)
        )
        if grades_highest.exists():
            for grade in grades_highest:
                total += (grade.grade * grade.module.weight)
                weighting_factor += grade.module.weight
            total = round(total / weighting_factor, 2)
            custom_students.append(CustomStudent(student, total))
            
    custom_students.sort(key=lambda x: x.average, reverse=True)
    if request.method == 'POST':
        enrolled_user_ids = request.POST.getlist('enrolled_users')  # Get a list of selected user IDs
        enrolled_users = User.objects.filter(id__in=enrolled_user_ids)
        for user in enrolled_users:
            EnrolledUser.objects.create(user=user, course=my_class)
    users = Account.objects.filter(is_teacher=False).exclude(
    user__in=EnrolledUser.objects.filter(course=my_class).values('user')
    )
    context = {'courseId': course_id, 'users': users, 'my_class': my_class, 'students': custom_students}
    return render(request, "teachers/course.html", context)

def studentView(request, course_id, student_id):
    course = MyClass.objects.get(id=course_id)
    student = User.objects.get(pk=student_id)
    custom_grades = []
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
        custom_grades.append(CustomGrade(module, grades))
    context = {'courseId': course_id, 'studentId': student_id, 'grades': custom_grades}
    return render(request, "teachers/studentview.html", context)

def attemptView(request, course_id, module_id, student_id, attempt):
    student = User.objects.get(pk=student_id)
    module = Module.objects.get(pk=module_id)
    questions = StudentQuestion.objects.filter(module=module, student=student, attempt=attempt)
    short_answers = StudentShortAnswer.objects.filter(module=module, student=student, attempt=attempt)
    for sh in short_answers:
        print(sh.grade)
    context = {'courseId': course_id, 'studentId': student_id, 'shortAnswers':short_answers, 'questions': questions, 'module':module}
    return render(request, "teachers/attemptview.html", context)

def deleteCourse(request, course_id):
    course = MyClass.objects.get(pk=course_id)
    course.delete()
    return redirect('teachers:home')
    
def discussion(request, course_id):
    my_class = MyClass.objects.get(id=course_id)
    messages = Discussion.objects.filter(course=my_class).order_by('-created_at')
    enrolled_users = EnrolledUser.objects.filter(course=my_class)
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
        return redirect(reverse('teachers:discussion', args=[course_id]))
        
    context = {'courseId': course_id, 'my_class': my_class, 'messages': messages}
    return render(request, "teachers/discussion.html", context)

def post(request, id, course_id):
    post = Discussion.objects.get(pk=id)
    fileName = ""
    if(post.file):
        fileName = post.file.name.split("/")[-1]
    replies = Reply.objects.filter(post=post).order_by('-created_at')
    if request.method == 'POST':
        message = request.POST.get('message')
        Reply.objects.create(post=post, author=request.user, message=message)
        return redirect(reverse('teachers:post', args=[id, course_id]))
    context = {'post':post, 'replies':replies, 'courseId':course_id, 'fileName':fileName}
    return render(request, "teachers/post.html", context)


def deletePost(request, id, course_id):
    post = Discussion.objects.get(pk=id)
    post.delete()
    return redirect(reverse('teachers:discussion', args=[course_id]))

def moduleHub(request, course_id):
    my_class = MyClass.objects.get(id=course_id)
    modules = Module.objects.filter(course=my_class).order_by('-created_at')
    if request.method == 'POST':
        title = request.POST.get('title')
        Module.objects.create(
            title = title,
            course=my_class, 
            author=request.user
        )
        return redirect(reverse('teachers:moduleHub', args=[course_id]))
        
    context = {'courseId': course_id, 'my_class': my_class, 'modules': modules}
    return render(request, "teachers/modulehub.html", context)

def module(request, id, course_id):
    module = Module.objects.get(pk=id)
    enrolled_students = EnrolledUser.objects.filter(course_id=course_id)
    student_progress = []
    for enrolled_student in enrolled_students:
        student = enrolled_student.user
        student_modules = StudentModule.objects.filter(student=student, module=module)
        if student_modules.exists():
            student_module = student_modules.first();
            student_progress.append(student_module)
            # update studentModule with new json data
        else:
            student_module = StudentModule.objects.create(
                module=module,
                student=student,
                progress=0,
            )
            student_progress.append(student_module)

    context = {"studentProgress":student_progress, "module":module, "courseId":course_id,}
    return render(request, "teachers/module.html", context)

def moduleSection(request, id, course_id):
    module = Module.objects.get(pk=id)
    questions = ModuleQuestion.objects.filter(module=module)
    sections = ModuleSection.objects.filter(module=module)
    shortAnswers = ShortAnswer.objects.filter(module=module)
    position = questions.count() + sections.count() + shortAnswers.count()
    prefabs = Prefab.objects.all()
    if request.method == 'POST':
        question = request.POST.get('question')
        image_url = request.POST.get('imageUrl')
        defaultModule = request.POST.get('defaultModule')
        uploaded_file = request.FILES.get('upload')
        selected_file = None;
        if(uploaded_file != None):
            selected_file = uploaded_file
        elif(image_url != None):
            selected_file = "prefabs/" + image_url
        ModuleSection.objects.create(
            module = module,
            text=question, 
            defaultModule=defaultModule,
            image=selected_file,
            position=position
        )
        return redirect(reverse('teachers:moduleSection', args=[id, course_id]))
    context = {"prefabs": prefabs, "questions":questions, "sections":sections, "module":module, "courseId":course_id, "count":range(position)}
    return render(request, "teachers/moduleview.html", context)

def shortAnswer(request, id, course_id):
    module = Module.objects.get(pk=id)
    questions = ModuleQuestion.objects.filter(module=module)
    sections = ModuleSection.objects.filter(module=module)
    shortAnswers = ShortAnswer.objects.filter(module=module)
    position = questions.count() + sections.count() + shortAnswers.count()
    if request.method == 'POST':
        question = request.POST.get('question')
        ShortAnswer.objects.create(
            module = module,
            question_text=question, 
            position=position
        )
    return redirect(reverse('teachers:moduleView', args=[id, course_id]))

def moduleView(request, id, course_id):
    module = Module.objects.get(pk=id)
    questions = ModuleQuestion.objects.filter(module=module)
    sections = ModuleSection.objects.filter(module=module)
    shortAnswers = ShortAnswer.objects.filter(module=module)
    position = questions.count() + sections.count() + shortAnswers.count()
    all_questions = []
    i = 0
    j = 0
    while i < questions.count() and j < shortAnswers.count():
        print(questions[i].position)
        print(shortAnswers[j].position)
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

    prefabs = Prefab.objects.all()
    if request.method == 'POST':
        question = request.POST.get('question')
        option1 = request.POST.get('option1')
        option2 = request.POST.get('option2')
        option3 = request.POST.get('option3')
        option4 = request.POST.get('option4')
        correct_answer = request.POST.get('correct_answer')
        ModuleQuestion.objects.create(
            module = module,
            question_text=question, 
            option1=option1,
            option2=option2,
            option3=option3,
            option4=option4,
            correct_answer= correct_answer,
            position=position
        )
        return redirect(reverse('teachers:moduleView', args=[id, course_id]))
    context = {"questions": all_questions, "prefabs": prefabs, "sections":sections, "module":module, "courseId":course_id, "count":range(position)}
    return render(request, "teachers/moduleview.html", context)

def studentModule(request, student_id, module_id):
    module = Module.objects.get(pk=module_id)
    course_id = module.course.id
    questions = ModuleQuestion.objects.filter(module=module)
    sections = ModuleSection.objects.filter(module=module)
    shortAnswers = ShortAnswer.objects.filter(module=module)
    position = questions.count() + sections.count() + shortAnswers.count()
    all_questions = []
    i = 0
    j = 0
    while i < questions.count() and j < shortAnswers.count():
        print(questions[i].position)
        print(shortAnswers[j].position)
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

    
    context = {"studentId":student_id, "questions":all_questions, "sections":sections, "module":module, "courseId":course_id, "count":range(position)}
    return render(request, "teachers/studentmodule.html", context)

def moduleOptions(request, id, course_id):
    module = Module.objects.get(pk=id)
    if request.method == 'POST':
        is_visible = request.POST.get('visible')
        weight = request.POST.get('gradeWeight')
        attempts = request.POST.get('attempts')
        if is_visible is None:
            is_visible = False
        module.is_visible = is_visible
        module.weight = weight  
        module.attempts = attempts 
        module.save()
        
        return redirect(reverse('teachers:moduleOptions', args=[id, course_id]))
    context = {"module":module, "courseId":course_id}
    return render(request, "teachers/moduleoptions.html", context)

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
        return redirect(reverse('teachers:quizHub', args=[course_id]))
        
    context = {'courseId': course_id, 'my_class': my_class, 'quizes': quizes}
    return render(request, "teachers/quizhub.html", context)

def quiz(request, id, course_id):
    quiz = Quiz.objects.get(pk=id)
    attempts = Grade.objects.filter(quiz=quiz)
    subquery = Grade.objects.filter(
    student=OuterRef('student'),
    quiz=quiz
    ).order_by('-grade').values('grade')[:1]

    grades = Grade.objects.filter(
    quiz=quiz,
    grade=Subquery(subquery)
    )
    context = {"quiz":quiz, "courseId":course_id, "grades":grades}
    return render(request, "teachers/quiz.html", context)

def quizView(request, id, course_id):
    quiz = Quiz.objects.get(pk=id)
    questions = Question.objects.filter(quiz=quiz)
    if request.method == 'POST':
        question = request.POST.get('question')
        option1 = request.POST.get('option1')
        option2 = request.POST.get('option2')
        option3 = request.POST.get('option3')
        option4 = request.POST.get('option4')
        correct_answer = request.POST.get('correct_answer')
        Question.objects.create(
            quiz = quiz,
            question_text=question, 
            option1=option1,
            option2=option2,
            option3=option3,
            option4=option4,
            correct_answer= correct_answer
        )
        return redirect(reverse('teachers:quizView', args=[id, course_id]))
    context = {"questions":questions, "quiz":quiz, "courseId":course_id}
    return render(request, "teachers/quizview.html", context)

def attempts(request, id, course_id, student_id):
    quiz = Quiz.objects.get(pk=id)
    student = User.objects.get(pk=student_id)
    grades = Grade.objects.filter(quiz=quiz, student=student)
    context = {"grades":grades, "quiz":quiz, "courseId":course_id}
    return render(request, "teachers/attempts.html", context)

def options(request, id, course_id):
    quiz = Quiz.objects.get(pk=id)
    if request.method == 'POST':
        is_visible = request.POST.get('visible')
        if is_visible is None:
            is_visible = False
        print(is_visible)
        weight = request.POST.get('gradeWeight')
        attempts = request.POST.get('attempts')
        quiz.is_visible = is_visible 
        quiz.weight = weight  
        quiz.attempts = attempts     
        quiz.save()
        return redirect(reverse('teachers:options', args=[id, course_id]))
    context = {"quiz":quiz, "courseId":course_id}
    return render(request, "teachers/options.html", context)

def deleteQuiz(requqest, id, course_id):
    quiz = Quiz.objects.get(pk=id)
    quiz.delete()
    return redirect(reverse('teachers:quizHub', args=[course_id]))

def deleteModule(requqest, id, course_id):
    module = Module.objects.get(pk=id)
    module.delete()
    return redirect(reverse('teachers:moduleHub', args=[course_id]))

def settings(request, url):
    context = {"url":url}
    return render(request, "teachers/settings.html", context)

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
            
        return redirect(reverse('teachers:settings', args=[url]))  # Redirect to the user's profile page or another appropriate page

def changePassword(request, url):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Update the session to prevent logging the user out
            messages.success(request, 'Password changed successfully.')
        else:
            messages.error(request, 'Could Not change password, Please Check length')
            return redirect(reverse('teachers:settings', args=[url]))  # Redirect to the user's profile page or another appropriate page

def analytics(request):
    custom_grades = []
    students = []
    courses = MyClass.objects.filter(teacher=request.user)
    student_ids = EnrolledUser.objects.filter(course__in=courses).values('user').distinct()

    for student in student_ids:
        students.append(User.objects.get(pk=student['user'])) 

    subquery = Grade.objects.filter(
        student=OuterRef('student'),
        module=OuterRef('module')
    ).order_by('-grade').values('grade')[:1]

    for course in courses:
        grades = []
        grade_counts = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
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
                letter_grade = ''
                for grade in grades_highest:
                    total += (grade.grade * grade.module.weight)
                    weighting_factor += grade.module.weight
                total = round(total / weighting_factor, 2)
                if total >= 90:
                    letter_grade = 'A'
                    grade_counts[letter_grade] += 1
                elif total >= 80:
                    letter_grade = 'B'
                    grade_counts[letter_grade] += 1
                elif total >= 70:
                    letter_grade = 'C'
                    grade_counts[letter_grade] += 1
                elif total >= 60:
                    letter_grade = 'D'
                    grade_counts[letter_grade] += 1
                else:
                    letter_grade = 'F'
                    grade_counts[letter_grade] += 1

                grades.append(letter_grade)
        custom_grades.append(CustomAnalytics(course,grades, grade_counts))

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = []
        for grade in custom_grades:
            data.append({
                'course_id': grade.course.id,
                'grade_counts': grade.grade_counts,
                'grade_check': len(grade.grades)
            })
        return JsonResponse(data, safe=False)
    context={'grades':custom_grades, 'students':students}
    return render(request, "teachers/analytics.html", context)

def studentReport(request, student_id):
    selected_student = User.objects.get(pk=student_id)
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
    context={'student_id':student_id, 'terms':terms}
    return render(request, "teachers/studentreport.html", context)

def submitGrade(request, course_id):
    course = MyClass.objects.get(pk=course_id)
    course_students = EnrolledUser.objects.filter(course=course)
    grades = []
    index = 0
    student_grade = 0

    subquery = Grade.objects.filter(
        student=OuterRef('student'),
        module=OuterRef('module')
    ).order_by('-grade').values('grade')[:1]

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
    for student in course_students:
        for grade in grades:
            print(grade.average)
            if grade.student == student.user:
                student_grade = grade.average
                break
            else:    
                index += 1
        percentile = round((index/len(grades))*100, 2)
        FinalGrade.objects.create(
            student=student.user, 
            course_name=course.class_name, 
            term=course.term,
            grade=student_grade, 
            percentile=percentile
        )
    return redirect(reverse('teachers:deleteCourse', args=[course_id]))

def pastSemester(request, student_id, term):
    student = User.objects.get(pk=student_id)
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
def moduleData(request, student_id, module_id):
    student = User.objects.get(pk=student_id)
    module = Module.objects.get(pk=module_id)
    studentModules = StudentModule.objects.filter(student=student, module=module)
    studentModule = None
    if studentModules.exists():
        studentModule = studentModules.first();
        # update studentModule with new json data
    else:
        studentModule = StudentModule.objects.create(
            module=module,
            student=student,
            progress=0,
        )
        
    input_values = studentModule.input_values
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        recievedData = json.loads(request.body)
        input_values = recievedData.get('input_values')
        progress = recievedData.get('progress')
        studentModule.input_values = input_values
        studentModule.progress = progress
        studentModule.save()
        return JsonResponse({'message': 'success'}, status = 200)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'input_values': input_values, 'progress':studentModule.progress}, safe=False)

def shortAnswerSubmissions(request, module_id, course_id):
    module = Module.objects.get(pk=module_id)
    short_answers = StudentShortAnswer.objects.filter(module=module)
    context={'module':module,'courseId':course_id, 'shortAnswers':short_answers}
    return render(request, "teachers/submissions.html", context)

def gradeSubmission(request, id):
    short_answer = StudentShortAnswer.objects.get(pk=id)
    questions = ModuleQuestion.objects.filter(module=short_answer.module)
    short_answers = ShortAnswer.objects.filter(module=short_answer.module)
    grades = Grade.objects.filter(module=short_answer.module, student=short_answer.student, attempt=short_answer.attempt)
    grade = None
    if grades.exists():
        grade = grades.first();
            
    total_questions = questions.count() + short_answers.count()
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        recievedData = json.loads(request.body)
        inputGrade = Decimal(recievedData.get('grade'))
        short_answer.grade = inputGrade
        short_answer.pending = False
        short_answer.save()
        answers_pending = StudentShortAnswer.objects.filter(module=short_answer.module, pending=True, attempt=short_answer.attempt)
        if grade != None:
            if answers_pending.count() == 0:
                grade.pending = False;
            grade.grade += inputGrade / total_questions
            print(total_questions)
            grade.save()
        
        return JsonResponse({'message': 'Grade submission successful'}, status = 200)
    
def screen1(request):
    return render(request, 'teachers/PremadeModules/HydroelectricDam/Screen1.html')

def animation1(request):
    return render(request, 'teachers/PremadeModules/HydroelectricDam/animation1.html')