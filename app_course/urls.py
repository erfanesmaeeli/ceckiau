from django.urls import path
from app_course import views

urlpatterns = [
    path('', views.courses, name="courses"),
    path('<str:slug>', views.course_detail, name="course-detail"),
    path('<str:course_slug>/<str:course_session_slug>', views.course_session_detail, name="course-session-detail"),
    # path('register/<int:course_id>', views.register_course, name="register-course"),
]
