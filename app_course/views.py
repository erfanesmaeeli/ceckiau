from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from app_course.models import Course , CourseSession
#from app_account.models import RegisteredCourse


def courses(request):
    ctx = {}
    ctx['courses'] = Course.objects.all().order_by('-id')
    return render(request, "courses.html" , ctx)


def course_detail(request, slug):
    ctx = {}
    ctx['course'] = get_object_or_404(Course, slug=slug)
    ctx['course_session'] = CourseSession.objects.filter(course__slug=slug).order_by("id")
    ctx['sessions_count'] = CourseSession.objects.filter(course__slug=slug).count()
    return render(request, "course-detail.html", ctx)


def course_session_detail(request, course_slug, course_session_slug):
    ctx = {}
    ctx['session'] = get_object_or_404(CourseSession, slug=course_session_slug)
    ctx['course_session'] = CourseSession.objects.filter(course__slug=course_slug).order_by("id")
    return render(request, "course-session-detail.html", ctx)


def register_course(request, course_slug):
    course = Course.objects.get(slug=course_slug)
    user = request.user
    if course not in [rc.course for rc in user.registeredcourse_set.all()]:
        user.registeredcourse_set.create(course=course)
        return HttpResponse("Done")
    return HttpResponse("exsit")


