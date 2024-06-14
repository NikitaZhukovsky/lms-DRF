from django.contrib import admin
from group.models import Group, StudentGroup, StudentLesson


class GroupAdmin(admin.ModelAdmin):
    list_display = ['course', 'name']
    search_fields = ['name']


class StudentLessonAdmin(admin.ModelAdmin):
    list_display = ['lesson', 'student', 'mark', 'attendance']


admin.site.register(Group, GroupAdmin)
admin.site.register(StudentLesson, StudentLessonAdmin)
