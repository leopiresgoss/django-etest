from django.db import models
from django.contrib.auth.models import User


# Models of the test creation
class Test(models.Model):
    
    name = models.CharField(max_length=120)
    test_code = models.SlugField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField()

    # The difference in minutes of the user's timezone and UTC
    tz = models.IntegerField(default=0)

    # To check if the test has been sended or editing yet
    sent = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)

    #def get_absolute_url(self):
        #return reverse("tests:test", kwargs={"pk": self.pk})
    
# Questions Model
class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    number = models.IntegerField()
    name = models.TextField()

    def __str__(self):
        return str(self.number)

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    number = models.IntegerField()
    option = models.TextField()
    correct_answer = models.BooleanField(default=False)

    def __str__(self):
        return self.option
    
