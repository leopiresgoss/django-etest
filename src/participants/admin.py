from django.contrib import admin
from .models import Participant, Participant_answer

# Register your models here.
admin.site.register(Participant)
admin.site.register(Participant_answer)