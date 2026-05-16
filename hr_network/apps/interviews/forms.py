from django import forms
from .models import Interview, InterviewParticipant, InterviewEvaluation
from apps.organization.models import Person, OrganizationalPost


class InterviewForm(forms.ModelForm):
    """
    فرم ایجاد/ویرایش جلسه مصاحبه
    """
    interviewer = forms.ModelChoiceField(
        queryset=Person.objects.all().order_by('first_name', 'last_name'),
        required=True,
        label="مصاحبه شونده (ارزیابی کننده)",
        widget=forms.Select(attrs={'class': 'form-select select2'})
    )

    class Meta:
        model = Interview
        fields = ['title', 'date', 'notes', 'interviewer']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'عنوان جلسه مصاحبه'}),
            'date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'yyyy/mm/dd'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'یادداشت‌های جلسه'}),
        }
        labels = {
            'title': 'عنوان جلسه',
            'date': 'تاریخ مصاحبه',
            'notes': 'یادداشت‌ها',
        }


class InterviewParticipantForm(forms.ModelForm):
    """
    فرم افزودن شرکت‌کننده به جلسه مصاحبه
    """
    class Meta:
        model = InterviewParticipant
        fields = ['interviewer', 'interviewer_post', 'notes']
        widgets = {
            'interviewer': forms.Select(attrs={'class': 'form-select'}),
            'interviewer_post': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
        labels = {
            'interviewer': 'مصاحبه‌شونده (ارزیابی‌کننده)',
            'interviewer_post': 'پست فرد',
            'notes': 'یادداشت',
        }


class InterviewEvaluationForm(forms.ModelForm):
    """
    فرم ارزیابی یک شایستگی
    """
    score = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(1, 6)],
        widget=forms.RadioSelect,
        label="نمره",
        required=False
    )
    
    class Meta:
        model = InterviewEvaluation
        fields = ['score', 'notes', 'selected_definition']
        widgets = {
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'توضیحات'}),
            'selected_definition': forms.HiddenInput(),
        }
        labels = {
            'score': 'نمره',
            'notes': 'توضیحات',
        }
