from django import forms
from .models import Competency, CompetencyLevel

class CompetencyForm(forms.ModelForm):
    class Meta:
        model = Competency
        fields = ['name', 'description']

class CompetencyLevelForm(forms.ModelForm):
    class Meta:
        model = CompetencyLevel
        fields = ['name', 'order']
