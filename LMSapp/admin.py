from django.contrib import admin
from django import forms

from .models import *
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin

admin.site.site_header = 'AUTHOR COURSE DASHBOARD'


class MyAdminSite(AdminSite):
    # Disable View on Site link on admin page
    view_on_site = True


class what_you_learn_TubulurinLine(admin.TabularInline):
    model = what_to_learn


class Video_TubulurinLine(admin.TabularInline):
    model = Video


class requirements_TublurinLine(admin.TabularInline):
    model = requirements


class course_admin(admin.ModelAdmin):
    inlines = (what_you_learn_TubulurinLine, requirements_TublurinLine, Video_TubulurinLine)
    list_display = ["title", "author"]

    def changelist_view(self, request, extra_context=None):
        queryset = self.get_queryset(request)

        if not queryset.exists():
            empty_message = "No courses found for the current user."
            context = {'empty_message': empty_message}
            return super().changelist_view(request, extra_context=context)

        return super().changelist_view(request, extra_context=extra_context)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset

        print(request.user)
        author_detail = Author.objects.filter(user_name=request.user)[0]
        print(author_detail)
        queryset = queryset.filter(author=author_detail)

        if not queryset.exists():
            return queryset.none()

        return queryset


class AuthorsAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        if request.user.is_superuser:
            return queryset

        print(request.user)
        return queryset.filter(user_name__startswith=request.user)


class LessonAdmin(admin.ModelAdmin):
    list_display = ["name", "course"]

    # readonly_fields = ('course',)

    def changelist_view(self, request, extra_context=None):
        queryset = self.get_queryset(request)

        if not queryset.exists():
            empty_message = "No courses found for the current user."
            context = {'empty_message': empty_message}
            return super().changelist_view(request, extra_context=context)

        return super().changelist_view(request, extra_context=extra_context)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset

        print(request.user)
        course_list = Course.objects.filter(author__user_name=request.user)
        print(course_list)
        queryset = queryset.filter(course__in=course_list)

        if not queryset.exists():
            return queryset.none()

        return queryset


class RequirementsAdmin(admin.ModelAdmin):
    list_display = ["points", "course"]
    readonly_fields = ('course',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset

        print(request.user)
        course_list = Course.objects.filter(author__user_name=request.user)
        print(course_list)
        queryset = queryset.filter(course__in=course_list)

        if not queryset.exists():
            return queryset.none()

        return queryset


class VideosAdmin(admin.ModelAdmin):
    list_display = ["title", "course"]

    # readonly_fields = ('course',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset

        print(request.user)
        course_list = Course.objects.filter(author__user_name=request.user)
        print(course_list)
        queryset = queryset.filter(course__in=course_list)

        if not queryset.exists():
            return queryset.none()

        return queryset

    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        return False


class WhatToLearnAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        # Check if the user is a superuser
        if request.user.is_superuser:
            return True
        return False


class LevelsAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        return False


# Register your models here.
admin.site.register(Categories)
admin.site.register(Course, course_admin)
admin.site.register(Author, AuthorsAdmin)
admin.site.register(Level, LevelsAdmin)
admin.site.register(what_to_learn, WhatToLearnAdmin)
admin.site.register(requirements, RequirementsAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Video, VideosAdmin)
admin.site.register(UserCourse)
