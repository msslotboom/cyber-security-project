from django.db import models
from django.contrib.auth.models import User


class Note(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	note_text = models.CharField(max_length=500)
	important = models.BooleanField(default=False)
	pub_date = models.DateTimeField("date published")

	def __str__(self):
		return self.note_text