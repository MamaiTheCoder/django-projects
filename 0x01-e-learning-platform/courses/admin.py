from django.contrib import admin

from .models import Subject, Course, Module

# Register your models here.

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}

# ModuleInline will allow you to manage Module instances directly within the Course admin page, making it convenient to add, edit, and remove modules associated with each course.    
class ModuleInline(admin.StackedInline):
    model = Module

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'created']
    list_filter = ['created', 'subject']
    search_fields = ['title', 'overview']
    prepopulated_fields = {'slug': ('title',)}
    # inlines = [ModuleInline]: Specifies that the Course admin page will include an inline interface for managing Module instances associated with each Course.
    inlines = [ModuleInline]