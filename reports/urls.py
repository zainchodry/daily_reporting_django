from django.urls import path
from .views import submit_report, my_reports, all_reports, report_detail, review_report, edit_report, delete_report

urlpatterns = [
    path('submit/', submit_report, name='submit_report'),
    path('my-reports/', my_reports, name='my_reports'),
    path('all/', all_reports, name='all_reports'),
    path('<int:pk>/', report_detail, name='report_detail'),
    path('<int:pk>/review/', review_report, name='review_report'),
    path('<int:pk>/edit/', edit_report, name='edit_report'),
    path('<int:pk>/delete/', delete_report, name='delete_report'),
]