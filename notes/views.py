from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from notes.models import Note

def index(request):
    latest_note_list = Note.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_note_list}
    return render(request, "polls/index.html", context)


def detail(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    return render(request, "polls/detail.html", {"question": note})