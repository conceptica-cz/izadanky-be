from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("user/", views.UserView.as_view(), name="user"),
]
