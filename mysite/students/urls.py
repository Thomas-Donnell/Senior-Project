from django.urls import path, re_path


from . import views
app_name = 'students'
urlpatterns = [
    path("", views.home, name="home"),
    path("course/<str:course_id>/", views.course, name="course"),
    path("delete_course/<str:course_id>/", views.deleteCourse, name="deleteCourse"),
    path("discussions/<str:course_id>/", views.discussion, name="discussion"),
    path("post/<str:id>/<str:course_id>/", views.post, name="post"),
    path("delete_post/<str:id>/<str:course_id>/", views.deletePost, name="deletePost"),
    path("quiz_hub/<str:course_id>/", views.quizHub, name="quizHub"),
    path("quiz/<str:id>/<str:course_id>/", views.quiz, name="quiz"),
    path("quiz_view/<str:id>/<str:course_id>/", views.quizView, name="quizView"),
    re_path(r'^settings/(?P<url>.+)/$', views.settings, name='settings'),
    re_path(r'^change_username/(?P<url>.+)/$', views.changeUsername, name='changeUsername'),
    re_path(r'^change_password/settings/(?P<url>.+)/$', views.changePassword, name='changePassword'),
    path("search/", views.search, name="search"),
    path("student_view/<str:course_id>/", views.studentView, name="studentView"),
    path("student_report/", views.studentReport, name="studentReport"),
    path("past_semester/<str:term>/", views.pastSemester, name="pastSemester"),

    path("anime/", views.anime, name="anime"),
]