from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from notes.models import Note
from django.contrib.auth.models import User
import requests

def index(request):
	if request.user.is_authenticated:
		latest_notes_list = Note.objects.filter(owner=request.user).order_by("-pub_date")[:5]
	else:
		latest_notes_list = []
	context = {"latest_notes_list": latest_notes_list}
	return render(request, "notes/index.html", context)

#Fix: uncomment line below
#@login_required
def detail(request, note_id):
	note = get_object_or_404(Note, pk=note_id)
	# Fix: comment line above, uncomment line below
	# note = get_object_or_404(Note, pk=note_id, owner=request.user)
	owner = get_object_or_404(User, pk=note.owner_id)
	return render(request, "notes/detail.html", {"note": note, "owner_name": owner.username})

# Fix for broken access control: uncomment line below
# @login_required
@csrf_exempt
def delete_note(request, note_id):
	note = get_object_or_404(Note, id=note_id)
	# Fix for broken access control: comment line above, uncomment line below
	# note = get_object_or_404(Note, id=note_id, owner=request.user)
	if note:
		note.delete()
	return redirect('index')

# Fix for csrf. It also has the fix for broken access control, for which the fix can also be found in the
# csrf-unsafe deletion method above.
#@login required
# def delete_note(request, note_id):
# 	if request.method == 'POST':
# 		note = get_object_or_404(Note, id=note_id)
# 		# Fix: comment line above, uncomment line below
# 		# note = get_object_or_404(Note, id=note_id, owner=request.user)
# 		note.delete()
# 		return redirect('index')
# 	else:
# 		return redirect('index')

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


# Note import that allows SSRF. Fix is commented in this function, and in template in frontend.
def import_note_from_url(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        # Fix for SSRF: Never trust urls given by users. The line below changes the design of this feature,
        # To only allow imports from an old note app, that is also owned by us, and the url form the form is
        # actually the note id.
        # url = "https://localhost:8001/notes/" + url
        print(url)
        try:
            response = requests.get(url)
            Note.objects.create(
                owner=request.user,
                note_text=response.text[:500],
                pub_date=timezone.now()
            )
        except:
            pass
        return redirect('index')
    return render(request, 'notes/import_note.html')


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
