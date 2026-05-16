from django import forms
from .models import FileArchive

class FileArchiveForm(forms.ModelForm):
    class Meta:
        model = FileArchive
        fields = ['original_filename', 'description']
