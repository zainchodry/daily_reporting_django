from django.db.models.signals import (
    post_save
)

from django.dispatch import receiver

from tasks.models import Task

from reports.models import DailyReport

from .models import Notification


@receiver(
    post_save,
    sender=Task
)
def task_assigned_notification(
    sender,
    instance,
    created,
    **kwargs
):

    if created:

        Notification.objects.create(
            receiver=instance.assigned_to,
            title="New Task Assigned",
            message=(
                f"You have been assigned task: "
                f"{instance.title}"
            ),
            notification_type="TASK_ASSIGNED"
        )

@receiver(
    post_save,
    sender=DailyReport
)
def report_review_notification(
    sender,
    instance,
    created,
    **kwargs
):

    if not created:

        if instance.status == "APPROVED":

            Notification.objects.create(
                receiver=instance.employee,
                title="Report Approved",
                message=(
                    "Your report has been approved"
                ),
                notification_type="REPORT_APPROVED"
            )

        elif instance.status == "REJECTED":

            Notification.objects.create(
                receiver=instance.employee,
                title="Report Rejected",
                message=(
                    "Your report has been rejected"
                ),
                notification_type="REPORT_REJECTED"
            )