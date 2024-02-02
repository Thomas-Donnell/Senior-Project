from django.contrib import admin
from .models import MyClass,  EnrolledUser, Discussion, Reply, Quiz, Question, Grade, Alert, StudentQuestion, FinalGrade
# Register your models here.
class MyClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'class_descriptor', 'class_name', 'teacher')
admin.site.register(MyClass, MyClassAdmin)
admin.site.register(EnrolledUser)
admin.site.register(Discussion)
admin.site.register(Reply)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Grade)
admin.site.register(Alert)
admin.site.register(StudentQuestion)
admin.site.register(FinalGrade)