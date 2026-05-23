from django.urls import path

from .views import *

urlpatterns = [

    path(
        "",
        notifications_list,
        name="notifications"
    ),

    path(
        "<int:pk>/",
        notification_detail,
        name="notification_detail"
    ),

    path(
        "mark-all-read/",
        mark_all_read,
        name="mark_all_read"
    ),
]