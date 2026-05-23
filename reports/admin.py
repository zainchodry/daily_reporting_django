from django.contrib import admin
from .models import DailyReport


@admin.register(DailyReport)
class DailyReportAdmin(admin.ModelAdmin):
    list_display = ('employee', 'task', 'report_date', 'hours_worked', 'status', 'created_at')
    list_filter = ('status', 'report_date', 'created_at')
    search_fields = ('employee__username', 'employee__email', 'task__title', 'work_summary')
    ordering = ('-report_date', '-created_at')
    date_hierarchy = 'report_date'
