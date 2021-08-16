from django.urls import path
from .views import start_test, test_question

#from .views import

app_name = 'participants'

urlpatterns = [
    path('<slug:test_code>', start_test, name='start-test'),
    path('<slug:test_code>/<int:num>', test_question, name='test-question'),
]