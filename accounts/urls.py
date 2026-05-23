from django.urls import path
from django.contrib.auth import views as auth_views

from .views import RegisterView, ProfileView, change_password, logout_view, dashboard
from .forms import LoginForm, ResetPasswordForm, SetNewPasswordForm

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('logout/', logout_view, name='logout'),
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html',
        authentication_form=LoginForm,
        redirect_authenticated_user=True,
    ), name='login'),
    path('change-password/', change_password, name='change_password'),

    # Password reset flow
    path('forget-password/', auth_views.PasswordResetView.as_view(
        template_name='accounts/forget_password.html',
        form_class=ResetPasswordForm,
        email_template_name='accounts/password_reset_email.html',
        success_url='/reset-password/done/',
    ), name='forget_password'),

    path('reset-password/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/reset_password_done.html',
    ), name='password_reset_done'),

    path('reset-password/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/reset_password_confirm.html',
        form_class=SetNewPasswordForm,
        success_url='/reset-password/complete/',
    ), name='password_reset_confirm'),

    path('reset-password/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/reset_password_complete.html',
    ), name='password_reset_complete'),
]
