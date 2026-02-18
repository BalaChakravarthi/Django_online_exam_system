from django.urls import path
from .views import exam_page, register, user_login, user_logout, exam_list,guest_login

urlpatterns = [
    path("", user_login, name="login"),
    path("register/", register, name="register"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("exams/", exam_list, name="exam_list"),   
    path("exam/<int:exam_id>/", exam_page, name="exam"),
    path("guest-login/", guest_login, name="guest_login"),
]

