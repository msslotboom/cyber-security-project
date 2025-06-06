from django.shortcuts import render
from django.http import HttpResponse
from notes.models import Note

def index(request):
    latest_note_list = Note.objects.order_by("-pub_date")[:5]
    output = ", ".join([n.note_text for n in latest_note_list])
    return HttpResponse(output)


def detail(request, note_id):
    return HttpResponse("You're looking at note %s." % note_id)