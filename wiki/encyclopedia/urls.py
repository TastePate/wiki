from django.urls import path
from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/", views.index, name="index"),
    path("wiki/<str:page_title>", views.wiki, name="wiki"),
    path("add/", views.add, name="add"),
    path("edit/<str:page_title>", views.edit, name="edit")
]