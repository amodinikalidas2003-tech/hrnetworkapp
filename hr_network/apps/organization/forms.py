from django import forms
from .models import OrganizationalPost, Department, Person, PersonPostHistory, PostLevel, ManagementLevel

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'parent', 'manager', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Department Name'}),
            'parent': forms.Select(attrs={'class': 'form-select'}),
            'manager': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description...'}),
        }

class OrganizationalPostForm(forms.ModelForm):
    class Meta:
        model = OrganizationalPost
        fields = ['title', 'department', 'post_level', 'parent_post', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job Title (e.g. HR Manager)'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'post_level': forms.Select(attrs={'class': 'form-select'}),
            'parent_post': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'national_id', 'phone_number', 'email', 'user', 'profile_picture']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'national_id': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'user': forms.Select(attrs={'class': 'form-select'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }

class PersonPostHistoryForm(forms.ModelForm):
    class Meta:
        model = PersonPostHistory
        fields = ['person', 'post', 'start_date', 'end_date', 'is_active']
        widgets = {
            'person': forms.Select(attrs={'class': 'form-select'}),
            'post': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ExcelImportForm(forms.Form):
    excel_file = forms.FileField(
        label="Excel File",
        help_text="Upload an Excel file (.xlsx) containing the data.",
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.xlsx, .xls'})
    )

class PostLevelForm(forms.ModelForm):
    """Form for creating/editing PostLevel - independent from CompetencyLevel"""
    class Meta:
        model = PostLevel
        fields = ['name', 'description', 'order', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ManagementLevelForm(forms.ModelForm):
    """Form for creating/editing ManagementLevel - independent from CompetencyLevel"""
    class Meta:
        model = ManagementLevel
        fields = ['name', 'description', 'level_number', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'level_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
