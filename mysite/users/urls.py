from django.urls import path

from . import views
app_name = 'users'
urlpatterns = [
    path("register/", views.register, name="register"),
    path("", views.loginPage, name="loginPage"),
    path("logout/", views.logoutPage, name="logoutPage"),
]