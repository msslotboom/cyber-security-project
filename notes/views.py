from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from notes.models import Note
from django.contrib.auth.models import User

def index(request):
	latest_notes_list = Note.objects.order_by("-pub_date")[:5]
	print(latest_notes_list)
	context = {"latest_notes_list": latest_notes_list}
	return render(request, "notes/index.html", context)


def detail(request, note_id):
	note = get_object_or_404(Note, pk=note_id)
	owner = get_object_or_404(User, pk=note.owner_id)
	return render(request, "notes/detail.html", {"note": note, "owner_name": owner.username})


def delete_note(request, note_id):
	note = Note.objects.get(id=note_id)
	note.delete()
	return redirect('index')

@login_required
def create_note(request):
	if request.method == 'POST':
		note_text = request.POST.get('note_text')
		if note_text:
			Note.objects.create(
				owner=request.user,
				note_text=note_text,
				pub_date=timezone.now()
			)
			return redirect('index')
	return render(request, 'notes/create_note.html')

class CustomLoginView(LoginView):
	# template_name = 'registration/login.html'
	redirect_authenticated_user = True
	success_url = reverse_lazy('index')

	def get_success_url(self):
		return reverse_lazy('index')

class CustomLogoutView(LogoutView):
	next_page = reverse_lazy('login')

	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

class CustomSignupView(CreateView):
	form_class = UserCreationForm
	template_name = 'registration/signup.html'
	success_url = reverse_lazy('index')

	def form_valid(self, form):
		response = super().form_valid(form)
		login(self.request, self.object)
		return response
