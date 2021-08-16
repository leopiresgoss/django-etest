from tests.models import Test
from datetime import datetime

# To check and return test and participant
def check_test_participant(request, test_code):
    test = Test.objects.filter(test_code=test_code, deadline__gte=datetime.now())
    participant = request.session.get('participant')
    
    return {'test': test, 'participant': participant}