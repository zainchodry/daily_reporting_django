from django import forms

from .models import Task


class TaskCreateForm(forms.ModelForm):

    class Meta:

        model = Task

        fields = [
            "title",
            "description",
            "assigned_to",
            "priority",
            "due_date"
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter task title"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter task description",
                    "rows": 4
                }
            ),

            "assigned_to": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "priority": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "due_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date"
                }
            ),
        }


class TaskStatusUpdateForm(forms.ModelForm):

    class Meta:

        model = Task

        fields = [
            "status"
        ]

        widgets = {
            "status": forms.Select(
                attrs={
                    "class": "form-select"
                }
            )
        }