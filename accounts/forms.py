from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)
from .models import User, Profile


class RegisterForm(UserCreationForm):
    """Custom registration form with email-based authentication."""

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter username',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address',
            }),
            'role': forms.Select(attrs={
                'class': 'form-select',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter password',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password',
        })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email


class LoginForm(AuthenticationForm):
    """
    Custom login form that uses email as the login credential.
    Django's AuthenticationForm uses 'username' field internally,
    so we customize the label and widget to show 'Email'.
    """
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter email address',
            'autofocus': True,
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password',
        })
    )


class ProfileForm(forms.ModelForm):
    """Profile update form."""

    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First name',
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last name',
        })
    )

    class Meta:
        model = Profile
        fields = ['phone', 'address', 'designation', 'image', 'bio', 'joined_date']

        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone number',
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Address',
                'rows': 3,
            }),
            'designation': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Job title / Designation',
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Tell us about yourself',
                'rows': 3,
            }),
            'joined_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name

    def save(self, commit=True):
        profile = super().save(commit=commit)
        if commit:
            user = profile.user
            user.first_name = self.cleaned_data.get('first_name', '')
            user.last_name = self.cleaned_data.get('last_name', '')
            user.save()
        return profile


class ChangePasswordForm(PasswordChangeForm):
    """Custom password change form with styled widgets."""

    old_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Current password',
    }))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'New password',
    }))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm new password',
    }))


class ResetPasswordForm(PasswordResetForm):
    """Password reset request form."""

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email address',
    }))


class SetNewPasswordForm(SetPasswordForm):
    """Set new password after reset form."""

    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'New password',
    }))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm new password',
    }))
