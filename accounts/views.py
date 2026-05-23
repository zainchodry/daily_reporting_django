from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout as auth_logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.db.models import Count, Q
from django.utils import timezone

from .forms import RegisterForm, ProfileForm, ChangePasswordForm
from .models import User, Profile
from tasks.models import Task
from reports.models import DailyReport
from notifications.models import Notification


class RegisterView(View):
    """User registration view."""

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        form = RegisterForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('login')
        return render(request, 'accounts/register.html', {'form': form})


class ProfileView(LoginRequiredMixin, View):
    """User profile view and update."""

    def get(self, request):
        profile = request.user.profile
        form = ProfileForm(instance=profile)
        return render(request, 'accounts/profile.html', {'form': form, 'profile': profile})

    def post(self, request):
        profile = request.user.profile
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        return render(request, 'accounts/profile.html', {'form': form, 'profile': profile})


@login_required
def change_password(request):
    """Change password view."""
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully!')
            return redirect('profile')
    else:
        form = ChangePasswordForm(request.user)
    return render(request, 'accounts/password_change.html', {'form': form})


@login_required
def logout_view(request):
    """Logout user (POST only for CSRF safety)."""
    if request.method == 'POST':
        auth_logout(request)
        messages.success(request, 'You have been logged out successfully.')
        return redirect('login')
    return redirect('dashboard')


@login_required
def dashboard(request):
    """Main dashboard view showing stats and recent activity."""
    user = request.user
    today = timezone.now().date()

    context = {
        'today': today,
    }

    if user.role in ['admin', 'manager']:
        # Manager/Admin stats
        context['total_tasks'] = Task.objects.count()
        context['pending_tasks'] = Task.objects.filter(status='PENDING').count()
        context['in_progress_tasks'] = Task.objects.filter(status='IN_PROGRESS').count()
        context['completed_tasks'] = Task.objects.filter(status='COMPLETED').count()
        context['total_reports'] = DailyReport.objects.count()
        context['pending_reports'] = DailyReport.objects.filter(status='SUBMITTED').count()
        context['total_employees'] = User.objects.filter(role='employee').count()
        context['recent_reports'] = DailyReport.objects.select_related(
            'employee', 'task'
        ).order_by('-created_at')[:5]
        context['recent_tasks'] = Task.objects.select_related(
            'assigned_by', 'assigned_to'
        ).order_by('-created_at')[:5]
    else:
        # Employee stats
        context['my_tasks'] = Task.objects.filter(assigned_to=user).count()
        context['my_pending_tasks'] = Task.objects.filter(
            assigned_to=user, status='PENDING'
        ).count()
        context['my_in_progress_tasks'] = Task.objects.filter(
            assigned_to=user, status='IN_PROGRESS'
        ).count()
        context['my_completed_tasks'] = Task.objects.filter(
            assigned_to=user, status='COMPLETED'
        ).count()
        context['my_reports_count'] = DailyReport.objects.filter(employee=user).count()
        context['my_approved_reports'] = DailyReport.objects.filter(
            employee=user, status='APPROVED'
        ).count()
        context['my_rejected_reports'] = DailyReport.objects.filter(
            employee=user, status='REJECTED'
        ).count()
        context['recent_reports'] = DailyReport.objects.filter(
            employee=user
        ).select_related('task').order_by('-created_at')[:5]
        context['recent_tasks'] = Task.objects.filter(
            assigned_to=user
        ).order_by('-created_at')[:5]

    context['unread_notifications'] = Notification.objects.filter(
        receiver=user, is_read=False
    ).count()

    return render(request, 'dashboard.html', context)
