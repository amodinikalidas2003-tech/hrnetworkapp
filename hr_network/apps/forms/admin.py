# Register your models here.

from django.contrib import admin
from .models import FormSchema, FormSubmission

@admin.register(FormSchema)
class FormSchemaAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'created_at')
    search_fields = ('name', 'description')

@admin.register(FormSubmission)
class FormSubmissionAdmin(admin.ModelAdmin):
    list_display = ('schema', 'submitted_by', 'created_at')
    list_filter = ('schema', 'created_at')
