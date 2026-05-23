from django.shortcuts import (
    render,
    get_object_or_404,
    redirect
)

from django.contrib.auth.decorators import (
    login_required
)

from .models import Notification


@login_required
def notifications_list(
    request
):

    notifications = (
        Notification.objects.filter(
            receiver=request.user
        ).order_by(
            "-created_at"
        )
    )

    context = {
        "notifications": notifications
    }

    return render(
        request,
        "notifications/notifications.html",
        context
    )

@login_required
def mark_all_read(
    request
):

    Notification.objects.filter(
        receiver=request.user,
        is_read=False
    ).update(
        is_read=True
    )

    return redirect(
        "notifications"
    )

@login_required
def notification_detail(
    request,
    pk
):

    notification = get_object_or_404(
        Notification,
        id=pk,
        receiver=request.user
    )

    notification.is_read = True

    notification.save()

    context = {
        "notification": notification
    }

    return render(
        request,
        "notifications/notification_detail.html",
        context
    )