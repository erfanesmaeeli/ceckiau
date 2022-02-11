from django.contrib import admin
from app_course.models import Course, CourseSession


class CourseAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'title', 'teacher', '_category', 'DateCreate', '_course_state', 'slug')
    list_editable = ('_course_state', 'slug')
    list_filter = ('title', '_category', 'teacher', '_course_state')
    search_fields = ('title', 'description', '_category', 'teacher', 'DateCreate')
    ordering = ['_course_state', '-DateCreate', 'title', 'teacher']

class CourseSessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'Course_Name', 'length', 'DateCreate', 'slug')
    list_editable = ('slug',)
    list_filter = ('course__title', 'DateCreate')
    search_fields = ('Course_Name', 'title', 'DateCreate')
    ordering = ['course__title', 'id', 'DateCreate', 'title']

    


admin.site.register(Course, CourseAdmin)
admin.site.register(CourseSession, CourseSessionAdmin)
# admin.site.register(AttachmentFiles)
