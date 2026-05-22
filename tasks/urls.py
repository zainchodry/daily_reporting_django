from django.urls import path

from .views import *

urlpatterns = [

    path(
        "",
        task_list,
        name="task_list"
    ),

    path(
        "create/",
        create_task,
        name="create_task"
    ),

    path(
        "my-tasks/",
        my_tasks,
        name="my_tasks"
    ),

    path(
        "<int:pk>/",
        task_detail,
        name="task_detail"
    ),

    path(
        "<int:pk>/update/",
        update_task_status,
        name="update_task_status"
    ),
]