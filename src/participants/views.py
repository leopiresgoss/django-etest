from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.db.models import F

from .forms import ParticipantForm
from .models import Participant, Participant_answer
from tests.models import Question, Option
from .helpers import check_test_participant

def start_test(request, test_code):
    # If test_code is not available and not
    results = check_test_participant(request, test_code)

    test = results['test']
    participant_id = results['participant']
    
    if not test or not test[0].sent:
        return HttpResponse("This test is not available")
    
    if participant_id:
        return HttpResponse("You cannot access this test. Please contact the responsible for your test.")

    form = ParticipantForm(request.POST or None)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')

        if form.is_valid():
            obj, created = Participant.objects.update_or_create(
                email=email, 
                test=test[0],
                defaults={
                    'name': name,
                    'email': email,
                    'test': test[0]
                })

            # if not created
            if not created:
                return HttpResponse("You cannot access this test. Please contact the responsible for your test.")
            
            request.session['participant'] = obj.id

            return redirect(f'{test_code}/1')
        else:
            """TODO MESSAGE"""
            return HttpResponse("Fill all fields correctly")
    
    context = {
        'form': form,
        'test': test[0],
    }

    return render(request, 'home.html', context)

def test_question(request, test_code, num):
    results = check_test_participant(request, test_code)
    test = results['test']
    participant_id = results['participant']

    if not test or not test[0].sent:
        return HttpResponse("This test is not available")

    # Check if this question exists
    question_query = Question.objects.filter(test=test[0], number=num)

    if not question_query:
        return HttpResponse("Question not found!")

    question = question_query[0]

    participant_query =  Participant.objects.filter(pk=participant_id)

    if not participant_query:
        HttpResponse("ERROR 404! NOT FOUND. Please contact the responsible for this test")

    participant = participant_query[0]

    # If it is the last question, it will be True
    # The last question will have only "finish test"
    finish_button = False

    last_question = Question.objects.filter(test=test[0]).order_by('-number')

    if last_question[0].id == question.id:
        finish_button = True

    # Check if it is the correct question to do
    last_question_answered = Participant_answer.objects.filter(
        test=test[0], participant=participant).order_by('-pk')

    # if last_question_answered and int(last_question_answered[0].question) + 1 != num:
    if last_question_answered:
        if last_question_answered[0].question.number + 1 != num:
            return HttpResponse('Invalid question**')
    elif num != 1:
        return HttpResponse('You should answer the questions ir order')

    # Get options
    options = Option.objects.filter(question=question)

    if request.method == 'POST':
        selected_option = request.POST.get('flexRadioDefault')
        
        if not selected_option:
            return HttpResponse('Select the correct answer')

        # Get option from selected_option
        for option in options:
            if option.number == int(selected_option):
                answer = Participant_answer(
                    test=test[0], 
                    participant=participant, 
                    question=question, 
                    answer=option)
                
                answer.save()

                if option.correct_answer:
                    participant_query.update(score=F('score') + 1)
        
        # It means the end of the test
        if finish_button:
            participant_query.update(finished=True)
            
            return render(request, 'test-finished.html')
        else:
            return redirect(f'/test/{test_code}/{num + 1}')


    for option in options:
        option.letter = f"{chr(97 + option.number)})"

    context = {
        'question': question,
        'options': options,
        'finish_button': finish_button
    }


    return render(request, 'question-participant.html', context)
