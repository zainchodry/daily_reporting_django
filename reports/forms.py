from django import forms
from .models import DailyReport
from tasks.models import Task


class DailyReportForm(forms.ModelForm):
    """Form for submitting daily reports."""

    class Meta:
        model = DailyReport
        fields = [
            'task',
            'report_date',
            'work_summary',
            'hours_worked',
            'blockers',
        ]

        widgets = {
            'task': forms.Select(attrs={
                'class': 'form-select',
            }),
            'report_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'work_summary': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe what you worked on today...',
                'rows': 4,
            }),
            'hours_worked': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 7.5',
                'step': '0.5',
                'min': '0',
                'max': '24',
            }),
            'blockers': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Any blockers or challenges? (optional)',
                'rows': 3,
            }),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            # Only show tasks assigned to this user
            self.fields['task'].queryset = Task.objects.filter(assigned_to=user)


class ReviewReportForm(forms.ModelForm):
    """Form for managers to review/approve/reject reports."""

    class Meta:
        model = DailyReport
        fields = [
            'status',
            'manager_feedback',
        ]

        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-select',
            }),
            'manager_feedback': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Provide feedback for the employee...',
                'rows': 4,
            }),
        }