from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_by', 'assigned_to', 'priority', 'status', 'due_date', 'created_at')
    list_filter = ('priority', 'status', 'due_date', 'created_at')
    search_fields = ('title', 'description', 'assigned_by__username', 'assigned_to__username')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
