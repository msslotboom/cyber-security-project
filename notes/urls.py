from django.urls import path

from . import views

urlpatterns = [
	path("", views.index, name="index"),
	path("<int:note_id>/", views.detail, name="detail"),
	path("delete/<int:note_id>/", views.delete_note, name="delete_note")
]