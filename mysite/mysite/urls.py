"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", include("users.urls")),
    path("students/", include("students.urls", "students")),
    path("teachers/", include("teachers.urls", "teachers")),
    path('admin/', admin.site.urls),

    # DC - Forgotten Password URLS

    #1 - User Email Submission - Utilizes djangos PasswordResetView (class based view)
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="users/reset_password.html"), name="reset_password"),
    #2 - Email Sent Message - Utilizes django PasswordResetDoneView (class based view)
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="users/reset_password_sent.html"), name="password_reset_done"),
    #3 - Email Link + Reset Instructions - Utilizes PasswordResetConfirmView (class based view)
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="users/reset.html"), name="password_reset_confirm"),
    #4 - Password Successfully Reset - Utilizes PasswordResetCompleteView (class based view)
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="users/reset_password_complete.html"), name="password_reset_complete"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
