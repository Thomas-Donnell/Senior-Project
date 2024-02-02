import uuid
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class MyClass(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    class_descriptor = models.CharField(max_length=50)
    class_name = models.CharField(max_length=100)
    term = models.CharField(max_length=100, null=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.class_name
    
    
class EnrolledUser(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(MyClass, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
    
class Discussion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(MyClass, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    file = models.FileField(upload_to='documents/', null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.subject
    
    def delete(self):
        self.file.delete()
        super().delete()
    
class Reply(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Discussion, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.post.subject
    
class Quiz(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(MyClass, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    is_visible = models.BooleanField(default=False)
    attempts = models.PositiveIntegerField(default=1)
    weight = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    
class Question(models.Model):
    id = models.AutoField(primary_key=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)
    correct_answer = models.IntegerField(choices=[(1, 'Option 1'), (2, 'Option 2'), (3, 'Option 3'), (4, 'Option 4')])

    def __str__(self):
        return self.quiz.title
    
class StudentQuestion(models.Model):
    id = models.AutoField(primary_key=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    attempt = models.PositiveIntegerField(default=0)
    correct_answer = models.IntegerField(choices=[(1, 'Option 1'), (2, 'Option 2'), (3, 'Option 3'), (4, 'Option 4')])
    selected_answer = models.IntegerField(choices=[(1, 'Option 1'), (2, 'Option 2'), (3, 'Option 3'), (4, 'Option 4')])

    def __str__(self):
        return self.quiz.title
    
class Grade(models.Model):
    id = models.AutoField(primary_key=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    grade = models.DecimalField(max_digits=5, decimal_places=2)
    attempt = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.quiz.title
    
class FinalGrade(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=100)
    term = models.CharField(max_length=100, null=True)
    grade = models.DecimalField(max_digits=5, decimal_places=2)
    percentile = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.student.username

class Alert(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(MyClass, on_delete=models.CASCADE)
    post = models.ForeignKey(Discussion, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.course.class_name