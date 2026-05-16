from django.contrib import admin
from .models import FileArchive

@admin.register(FileArchive)
class FileArchiveAdmin(admin.ModelAdmin):
    list_display = ('original_filename', 'uploaded_by', 'size', 'content_type', 'created_at')
    search_fields = ('original_filename', 'description')
    list_filter = ('content_type', 'created_at')
