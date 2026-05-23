from notifications.models import Notification


def notifications_count(request):
    """
    Context processor that adds unread notification count to all templates.
    Used in the navbar to show a badge.
    """
    if request.user.is_authenticated:
        count = Notification.objects.filter(
            receiver=request.user,
            is_read=False
        ).count()
        return {'unread_notifications_count': count}
    return {'unread_notifications_count': 0}
