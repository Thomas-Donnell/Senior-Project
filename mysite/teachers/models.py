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

class Module(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(MyClass, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    is_visible = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class ModuleSection(models.Model):
    id = models.AutoField(primary_key=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    defaultModule = models.CharField(max_length=100, null=True)
    text = models.CharField(max_length=200)
    position = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.module.title

class ModuleQuestion(models.Model):
    id = models.AutoField(primary_key=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200, null=True, blank=True)
    option1 = models.CharField(max_length=100, null=True)
    option2 = models.CharField(max_length=100, null=True)
    option3 = models.CharField(max_length=100, null=True)
    option4 = models.CharField(max_length=100, null=True)
    correct_answer = models.IntegerField(choices=[(1, 'Option 1'), (2, 'Option 2'), (3, 'Option 3'), (4, 'Option 4')], null=True)
    position = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.module.title
      
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
    
class ShortAnswer(models.Model):
    id = models.AutoField(primary_key=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=500)
    position = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.module.title
    
    
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
    
class StudentModule(models.Model):
    id = models.AutoField(primary_key=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    input_values = models.JSONField(null=True)
    progress = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    def __str__(self):
        return f"{self.student.username} - {self.module.title}"
    
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
    
class Prefab(models.Model):
    id = models.AutoField(primary_key=True)
    prefab = models.ImageField(null=True, blank=True, upload_to='prefabs/')

    def __str__(self):
        return str(self.id)