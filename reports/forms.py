from django import forms

from .models import DailyReport


class DailyReportForm(forms.ModelForm):

    class Meta:

        model = DailyReport

        fields = [
            "task",
            "report_date",
            "work_summary",
            "hours_worked",
            "blockers"
        ]

        widgets = {
            "task": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "report_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date"
                }
            ),

            "work_summary": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter work summary",
                    "rows": 4
                }
            ),

            "hours_worked": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter hours worked",
                    "step": "0.5"
                }
            ),

            "blockers": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter blockers if any",
                    "rows": 3
                }
            ),
        }


class ReviewReportForm(forms.ModelForm):

    class Meta:

        model = DailyReport

        fields = [
            "status",
            "manager_feedback"
        ]

        widgets = {
            "status": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "manager_feedback": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter manager feedback",
                    "rows": 4
                }
            ),
        }