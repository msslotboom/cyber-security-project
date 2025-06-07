from django.urls import path

from . import views

urlpatterns = [
	path("", views.index, name="index"),
	path("<int:note_id>/", views.detail, name="detail"),
	path("delete/<int:note_id>/", views.delete_note, name="delete_note"),
	path("login/", views.CustomLoginView.as_view(), name="login"),
	path("logout/", views.CustomLogoutView.as_view(), name="logout"),
	path("signup/", views.CustomSignupView.as_view(), name="signup"),
	path("create/", views.create_note, name="create_note"),
]