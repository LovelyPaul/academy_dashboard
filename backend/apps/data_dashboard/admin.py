"""
Django admin configuration for data dashboard app.
"""
from django.contrib import admin
from .models import DepartmentKPI, Publication, Student, ResearchBudgetData, UploadHistory


@admin.register(DepartmentKPI)
class DepartmentKPIAdmin(admin.ModelAdmin):
    list_display = ('year', 'college', 'department', 'employment_rate')
    list_filter = ('year', 'college')
    search_fields = ('college', 'department')


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('publication_id', 'title', 'publication_date', 'journal_name')
    list_filter = ('publication_date', 'journal_grade')
    search_fields = ('title', 'primary_author', 'journal_name')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'name', 'department', 'enrollment_status')
    list_filter = ('program_type', 'enrollment_status', 'admission_year')
    search_fields = ('student_id', 'name', 'email')


@admin.register(ResearchBudgetData)
class ResearchBudgetDataAdmin(admin.ModelAdmin):
    list_display = ('execution_id', 'project_name', 'execution_date', 'execution_amount')
    list_filter = ('status', 'execution_date')
    search_fields = ('project_number', 'project_name', 'principal_investigator')


@admin.register(UploadHistory)
class UploadHistoryAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'file_type', 'status', 'records_processed', 'uploaded_at')
    list_filter = ('file_type', 'status', 'uploaded_at')
    search_fields = ('file_name',)
    readonly_fields = ('uploaded_at',)
