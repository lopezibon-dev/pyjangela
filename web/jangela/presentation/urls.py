from django.urls import path

from jangela.presentation import views

urlpatterns = [
    path("", views.hasiera, name="hasiera"),
]
