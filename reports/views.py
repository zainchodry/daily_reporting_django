from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import (
    login_required
)

from django.contrib import messages

from .models import DailyReport

from .forms import (
    DailyReportForm,
    ReviewReportForm
)


@login_required
def submit_report(
    request
):

    form = DailyReportForm()

    if request.method == "POST":

        form = DailyReportForm(
            request.POST
        )

        if form.is_valid():

            report = form.save(
                commit=False
            )

            report.employee = (
                request.user
            )

            existing_report = (
                DailyReport.objects.filter(
                    employee=request.user,
                    task=report.task,
                    report_date=report.report_date
                ).exists()
            )

            if existing_report:

                messages.error(
                    request,
                    "You already submitted report for this task today"
                )

                return redirect(
                    "submit_report"
                )

            report.save()

            messages.success(
                request,
                "Daily report submitted successfully"
            )

            return redirect(
                "my_reports"
            )

    context = {
        "form": form
    }

    return render(
        request,
        "reports/submit_report.html",
        context
    )

@login_required
def my_reports(
    request
):

    reports = (
        DailyReport.objects.filter(
            employee=request.user
        ).order_by(
            "-created_at"
        )
    )

    context = {
        "reports": reports
    }

    return render(
        request,
        "reports/my_reports.html",
        context
    )

@login_required
def all_reports(
    request
):

    if request.user.role not in [
        "ADMIN",
        "MANAGER"
    ]:

        messages.error(
            request,
            "Permission denied"
        )

        return redirect(
            "my_reports"
        )

    reports = (
        DailyReport.objects.all()
        .order_by("-created_at")
    )

    context = {
        "reports": reports
    }

    return render(
        request,
        "reports/all_reports.html",
        context
    )

@login_required
def report_detail(
    request,
    pk
):

    report = get_object_or_404(
        DailyReport,
        id=pk
    )

    context = {
        "report": report
    }

    return render(
        request,
        "reports/report_detail.html",
        context
    )

@login_required
def review_report(
    request,
    pk
):

    if request.user.role not in [
        "ADMIN",
        "MANAGER"
    ]:

        messages.error(
            request,
            "Permission denied"
        )

        return redirect(
            "all_reports"
        )

    report = get_object_or_404(
        DailyReport,
        id=pk
    )

    form = ReviewReportForm(
        instance=report
    )

    if request.method == "POST":

        form = ReviewReportForm(
            request.POST,
            instance=report
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Report reviewed successfully"
            )

            return redirect(
                "all_reports"
            )

    context = {
        "form": form,
        "report": report
    }

    return render(
        request,
        "reports/review_report.html",
        context
    )

