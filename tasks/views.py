from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Task
from .forms import TaskCreateForm, TaskStatusUpdateForm
from accounts.decorators import role_required


@login_required
@role_required('admin', 'manager')
def create_task(request):
    """Create a new task (admin/manager only)."""
    form = TaskCreateForm()

    if request.method == 'POST':
        form = TaskCreateForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.assigned_by = request.user
            task.save()
            messages.success(request, 'Task created successfully!')
            return redirect('task_list')

    return render(request, 'tasks/create_task.html', {'form': form})


@login_required
def task_list(request):
    """List all tasks (admin/manager see all, employees see their own)."""
    if request.user.role in ['admin', 'manager']:
        tasks = Task.objects.select_related(
            'assigned_by', 'assigned_to'
        ).all().order_by('-created_at')
    else:
        tasks = Task.objects.filter(
            assigned_to=request.user
        ).select_related('assigned_by').order_by('-created_at')

    return render(request, 'tasks/task_list.html', {'tasks': tasks})


@login_required
def my_tasks(request):
    """List tasks assigned to current user."""
    tasks = Task.objects.filter(
        assigned_to=request.user
    ).select_related('assigned_by').order_by('-created_at')

    return render(request, 'tasks/my_tasks.html', {'tasks': tasks})


@login_required
def task_detail(request, pk):
    """View task details."""
    task = get_object_or_404(Task, id=pk)

    # Employees can only see their own tasks
    if request.user.role == 'employee' and task.assigned_to != request.user:
        messages.error(request, 'Permission denied.')
        return redirect('my_tasks')

    return render(request, 'tasks/task_detail.html', {'task': task})


@login_required
def update_task_status(request, pk):
    """Update task status (assigned employee only)."""
    task = get_object_or_404(Task, id=pk)

    if task.assigned_to != request.user and request.user.role not in ['admin', 'manager']:
        messages.error(request, 'Permission denied.')
        return redirect('my_tasks')

    form = TaskStatusUpdateForm(instance=task)

    if request.method == 'POST':
        form = TaskStatusUpdateForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task status updated successfully!')
            return redirect('my_tasks')

    return render(request, 'tasks/update_task.html', {'form': form, 'task': task})


@login_required
@role_required('admin', 'manager')
def delete_task(request, pk):
    """Delete a task (admin/manager only, POST required)."""
    task = get_object_or_404(Task, id=pk)

    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('task_list')

    return redirect('task_detail', pk=pk)
