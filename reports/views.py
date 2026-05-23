from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import DailyReport
from .forms import DailyReportForm, ReviewReportForm
from accounts.decorators import role_required


@login_required
def submit_report(request):
    """Submit a daily report."""
    form = DailyReportForm(user=request.user)

    if request.method == 'POST':
        form = DailyReportForm(request.POST, user=request.user)

        if form.is_valid():
            report = form.save(commit=False)
            report.employee = request.user

            existing = DailyReport.objects.filter(
                employee=request.user,
                task=report.task,
                report_date=report.report_date
            ).exists()

            if existing:
                messages.error(request, 'You already submitted a report for this task on this date.')
                return redirect('submit_report')

            report.save()
            messages.success(request, 'Daily report submitted successfully!')
            return redirect('my_reports')

    return render(request, 'reports/submit_report.html', {'form': form})


@login_required
def my_reports(request):
    """List current user's reports."""
    reports = DailyReport.objects.filter(
        employee=request.user
    ).select_related('task').order_by('-report_date', '-created_at')

    return render(request, 'reports/my_reports.html', {'reports': reports})


@login_required
@role_required('admin', 'manager')
def all_reports(request):
    """List all reports (admin/manager only)."""
    reports = DailyReport.objects.select_related(
        'employee', 'task'
    ).all().order_by('-report_date', '-created_at')

    return render(request, 'reports/all_reports.html', {'reports': reports})


@login_required
def report_detail(request, pk):
    """View report details."""
    report = get_object_or_404(DailyReport, id=pk)

    # Employees can only view their own reports
    if request.user.role == 'employee' and report.employee != request.user:
        messages.error(request, 'Permission denied.')
        return redirect('my_reports')

    return render(request, 'reports/report_detail.html', {'report': report})


@login_required
@role_required('admin', 'manager')
def review_report(request, pk):
    """Review/approve/reject a report (admin/manager only)."""
    report = get_object_or_404(DailyReport, id=pk)
    form = ReviewReportForm(instance=report)

    if request.method == 'POST':
        form = ReviewReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            messages.success(request, 'Report reviewed successfully!')
            return redirect('all_reports')

    return render(request, 'reports/review_report.html', {'form': form, 'report': report})


@login_required
def edit_report(request, pk):
    """Edit a report (only if still SUBMITTED status)."""
    report = get_object_or_404(DailyReport, id=pk, employee=request.user)

    if report.status != 'SUBMITTED':
        messages.error(request, 'You can only edit reports that are still pending review.')
        return redirect('my_reports')

    form = DailyReportForm(instance=report, user=request.user)

    if request.method == 'POST':
        form = DailyReportForm(request.POST, instance=report, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Report updated successfully!')
            return redirect('my_reports')

    return render(request, 'reports/submit_report.html', {
        'form': form,
        'editing': True,
        'report': report,
    })


@login_required
def delete_report(request, pk):
    """Delete a report (only if still SUBMITTED status, POST required)."""
    report = get_object_or_404(DailyReport, id=pk, employee=request.user)

    if report.status != 'SUBMITTED':
        messages.error(request, 'You can only delete reports that are still pending review.')
        return redirect('my_reports')

    if request.method == 'POST':
        report.delete()
        messages.success(request, 'Report deleted successfully!')
        return redirect('my_reports')

    return redirect('report_detail', pk=pk)
