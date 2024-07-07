from django.contrib import admin
from catalog.models import Course, CourseModule, Lesson, LessonContent, StudentCourse, CourseImage


class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'format', 'date_start', 'date_end', 'teacher']
    search_fields = ['title', 'format']


class CourseModuleAdmin(admin.ModelAdmin):
    list_display = ['course', 'title']
    search_fields = ['title']


class StudentCourseAdmin(admin.ModelAdmin):
    list_display = ['student', 'course']


class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'module', 'type', 'date_time']
    search_fields = ['title', 'type']


class LessonContentAdmin(admin.ModelAdmin):
    list_display = ['lesson', 'name']


class CourseImageAdmin(admin.ModelAdmin):
    list_display = ['course', 'name']


admin.site.register(Course, CourseAdmin)
admin.site.register(CourseModule, CourseModuleAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(CourseImage, CourseImageAdmin)
admin.site.register(StudentCourse, StudentCourseAdmin)
admin.site.register(LessonContent, LessonContentAdmin)
