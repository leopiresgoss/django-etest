from django.db import models
from tests.models import Test, Question, Option

# Create your models here.
class Participant(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(max_length=254)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    finished = models.BooleanField(default=False)
    score = models.FloatField(default=0.0)
    

    def __str__(self):
        return str(self.name)

class Participant_answer(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Option, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.participant} answer of {self.question}"




