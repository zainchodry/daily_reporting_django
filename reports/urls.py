from django.urls import path

from .views import *

urlpatterns = [

    path(
        "submit/",
        submit_report,
        name="submit_report"
    ),

    path(
        "my-reports/",
        my_reports,
        name="my_reports"
    ),

    path(
        "all/",
        all_reports,
        name="all_reports"
    ),

    path(
        "<int:pk>/",
        report_detail,
        name="report_detail"
    ),

    path(
        "<int:pk>/review/",
        review_report,
        name="review_report"
    ),
]