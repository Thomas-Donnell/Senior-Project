from django.urls import path, re_path


from . import views
app_name = 'teachers'
urlpatterns = [
    path("", views.home, name="home"),
    path("course/<str:course_id>/", views.course, name="course"),
    path("delete_course/<str:course_id>/", views.deleteCourse, name="deleteCourse"),
    path("discussions/<str:course_id>/", views.discussion, name="discussion"),
    path("post/<str:id>/<str:course_id>/", views.post, name="post"),
    path("delete_post/<str:id>/<str:course_id>/", views.deletePost, name="deletePost"),
    path("module_hub/<str:course_id>/", views.moduleHub, name="moduleHub"),
    path("module/<str:id>/<str:course_id>/", views.module, name="module"),
    path("module_view/<str:id>/<str:course_id>/", views.moduleView, name="moduleView"),
    path("module_section/<str:id>/<str:course_id>/", views.moduleSection, name="moduleSection"),
    path("short_answer/<str:id>/<str:course_id>/", views.shortAnswer, name="shortAnswer"),
    path("quiz_hub/<str:course_id>/", views.quizHub, name="quizHub"),
    path("quiz/<str:id>/<str:course_id>/", views.quiz, name="quiz"),
    path("quiz_view/<str:id>/<str:course_id>/", views.quizView, name="quizView"),
    path("options/<str:id>/<str:course_id>/", views.options, name="options"),
    path("module_options/<str:id>/<str:course_id>/", views.moduleOptions, name="moduleOptions"),
    path("submissions/<str:module_id>/<str:course_id>/", views.shortAnswerSubmissions, name="shortAnswerSubmissions"),
    path("delete_quiz/<str:id>/<str:course_id>/", views.deleteQuiz, name="deleteQuiz"),
    path("delete_module/<str:id>/<str:course_id>/", views.deleteModule, name="deleteModule"),
    re_path(r'^settings/(?P<url>.+)/$', views.settings, name='settings'),
    re_path(r'^change_username/(?P<url>.+)/$', views.changeUsername, name='changeUsername'),
    re_path(r'^change_password/settings/(?P<url>.+)/$', views.changePassword, name='changePassword'),
    path("search/", views.search, name="search"),
    path("attempts/<str:id>/<str:course_id>/<int:student_id>/", views.attempts, name="attempts"),
    path("student_view/<str:course_id>/<int:student_id>/", views.studentView, name="studentView"),
    path("attempt_view/<str:course_id>/<str:module_id>/<int:student_id>/<int:attempt>/", views.attemptView, name="attemptView"),
    path("analytics/", views.analytics, name="analytics"),
    path("student_report/<int:student_id>/", views.studentReport, name="studentReport"),
    path("submit_grade/<str:course_id>/", views.submitGrade, name="submitGrade"),
    path("past_semester/<int:student_id>/<str:term>/", views.pastSemester, name="pastSemester"),
    path("module_data/<int:student_id>/<str:module_id>/", views.moduleData, name="moduleData"),
    path("student_module/<int:student_id>/<str:module_id>/", views.studentModule, name="studentModule"),
    path("grade_submission/<int:id>/", views.gradeSubmission, name="gradeSubmission"),
    path("delete_section/<int:section_id>/", views.deleteSection, name="deleteSection"),
    path("delete_shortanswer/<str:id>/", views.deleteShortAnswer, name="deleteShortAnswer"),
    path("delete_multichoice/<str:id>/", views.deleteMultiChoice, name="deleteMultiChoice"),
    path('screen1/', views.screen1, name='screen1'),
    path('animation1/', views.animation1, name='animation1'),
]   
