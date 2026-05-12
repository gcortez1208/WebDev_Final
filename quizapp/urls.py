from django.urls import path

from . import views

urlpatterns = [
    path("", views.homepage, name="index"),
    path("submit/", views.submit_answer, name="submit"),
]
