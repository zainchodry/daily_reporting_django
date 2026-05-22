from django.db import models

from accounts.models import User

from tasks.models import Task


class DailyReport(
    models.Model
):

    STATUS_CHOICES = (
        ("SUBMITTED", "Submitted"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    )

    employee = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE
    )

    report_date = models.DateField()

    work_summary = models.TextField()

    hours_worked = models.DecimalField(
        max_digits=4,
        decimal_places=2
    )

    blockers = models.TextField(
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="SUBMITTED"
    )

    manager_feedback = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        unique_together = (
            "employee",
            "task",
            "report_date"
        )

    def __str__(self):

        return (
            f"{self.employee.email}"
            f" - {self.report_date}"
        )