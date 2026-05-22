from django.urls import path
from . views import *
from django.contrib.auth import views as auth_views
from . forms import *

urlpatterns = [
    path('', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('logout/', logout, name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html', authentication_form=LoginForm), name='login'),
    path('change-password/', ChangePasswordView, name='change-password'),
    path('change-password/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password-change-done'),
    path('forget-password/', auth_views.PasswordResetView.as_view(template_name='forget-password.html', form_class=ResetPasswordForm), name='forget-password'),
    path('reset-password/done/', auth_views.PasswordResetDoneView.as_view(template_name='reset_password_done.html'), name='reset_password_done'),
    path('reset-password-/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='reset_password_confirm.html', form_class=SetNewPasswordForm), name='reset_password_confirm'),
    path('reset_password/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='reset_password_complete.html'), name='reset_password_complete')
    
]
