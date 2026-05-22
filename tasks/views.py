from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import (
    login_required
)

from django.contrib import messages

from .models import Task

from .forms import (
    TaskCreateForm,
    TaskStatusUpdateForm
)


@login_required
def create_task(
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
            "task_list"
        )

    form = TaskCreateForm()

    if request.method == "POST":

        form = TaskCreateForm(
            request.POST
        )

        if form.is_valid():

            task = form.save(
                commit=False
            )

            task.assigned_by = (
                request.user
            )

            task.save()

            messages.success(
                request,
                "Task created successfully"
            )

            return redirect(
                "task_list"
            )

    context = {
        "form": form
    }

    return render(
        request,
        "tasks/create_task.html",
        context
    )

@login_required
def task_list(
    request
):

    if request.user.role in [
        "ADMIN",
        "MANAGER"
    ]:

        tasks = Task.objects.all()

    else:

        tasks = Task.objects.filter(
            assigned_to=request.user
        )

    context = {
        "tasks": tasks
    }

    return render(
        request,
        "tasks/task_list.html",
        context
    )

@login_required
def my_tasks(
    request
):

    tasks = Task.objects.filter(
        assigned_to=request.user
    )

    context = {
        "tasks": tasks
    }

    return render(
        request,
        "tasks/my_tasks.html",
        context
    )

@login_required
def task_detail(
    request,
    pk
):

    task = get_object_or_404(
        Task,
        id=pk
    )

    context = {
        "task": task
    }

    return render(
        request,
        "tasks/task_detail.html",
        context
    )

@login_required
def update_task_status(
    request,
    pk
):

    task = get_object_or_404(
        Task,
        id=pk
    )

    if task.assigned_to != request.user:

        messages.error(
            request,
            "Permission denied"
        )

        return redirect(
            "my_tasks"
        )

    form = TaskStatusUpdateForm(
        instance=task
    )

    if request.method == "POST":

        form = TaskStatusUpdateForm(
            request.POST,
            instance=task
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Task updated successfully"
            )

            return redirect(
                "my_tasks"
            )

    context = {
        "form": form
    }

    return render(
        request,
        "tasks/update_task.html",
        context
    )

