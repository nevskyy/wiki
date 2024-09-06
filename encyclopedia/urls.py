from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.show_entry_page, name="show_entry_page"),
    path("search", views.search, name="search"),
    path("new", views.new_page, name="new_page"),
    path("edit", views.edit_page, name="edit_page"),
    path("save_edit", views.save_edit, name="save_edit"),
    path("random", views.show_random_page, name="show_random_page"),
]
