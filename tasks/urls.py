from django.urls import path
from .views import task_list, create_task, my_tasks, task_detail, update_task_status, delete_task

urlpatterns = [
    path('', task_list, name='task_list'),
    path('create/', create_task, name='create_task'),
    path('my-tasks/', my_tasks, name='my_tasks'),
    path('<int:pk>/', task_detail, name='task_detail'),
    path('<int:pk>/update/', update_task_status, name='update_task_status'),
    path('<int:pk>/delete/', delete_task, name='delete_task'),
]