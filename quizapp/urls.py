from django.urls import path

from . import views

urlpatterns = [
    path("", views.homepage, name="index"),
    path("process/", views.process_form, name="process_form"),
    path("submit/", views.process_form, name="submit"),
]
