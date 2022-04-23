from django.urls import path

from . import views

app_name = "common"

urlpatterns = [
    path(
        "tasks/<str:task_id>/",
        views.TaskView.as_view(),
        name="task",
    ),
]
