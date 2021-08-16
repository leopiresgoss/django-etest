from django.db.models.fields import SlugField
from django.http.response import HttpResponse
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from uuid import uuid4

from .forms import CreateForm
from datetime import datetime, timedelta

from .models import Question, Test, Option
from .helpers import update_participants_query
from participants.models import Participant, Participant_answer

class TestsListView(LoginRequiredMixin, ListView):
    template_name = 'index.html'
    
    # to the query resulted be only by the current user
    def get_queryset(self):
        query = Test.objects.filter(user=self.request.user)

        if query:
            for test in query:
                # to update deadline by the user's timezone
                test.deadline -= timedelta(minutes=test.tz) 
                
        return query
    
    # To send user_is_logged = True to html
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        context['user_is_logged'] = True
        
        return context

@login_required
def test_creation(request):
    form = CreateForm(request.POST or None)
    
    context = {
        'form': form, 
        'user_is_logged': True
    }

    if request.method == 'POST':
        name = request.POST.get('name')
        user = request.user

        deadline_date = request.POST.get('deadline_date')
        deadline_time = request.POST.get('deadline_time')

        deadline_str = deadline_date + " " + deadline_time

        test_code = uuid4()

        # Get the difference between UTC and local timezone in minutes
        tz = int(request.POST.get('client_timezone'))

        # Create deadline as a datetime (year, month, day, hour, minutes)
        deadline = datetime.strptime(deadline_str, '%Y-%m-%d %H:%M')

        # Update the deadline by the tz
        # To avoid problems when saving in the database
        deadline += timedelta(minutes=tz)

        now = datetime.now()

        if deadline <= now:
            context['error'] = 'The deadline must not be before now'
            return render(request, 'create.html', context)

        # Insert into db
        if form.is_valid():
            t = Test(name=name, user=user, test_code=test_code, deadline=deadline, tz=tz)
            t.save()
            
            return redirect(f'{t.test_code}/1')

    
    return render(request, 'create.html', context)

# Create questions views
@login_required
def questions_creation(request, test_code, num):
    try:
        question_name = None
        options = list()
        context = {
            'num': num,
            'user_is_logged': True
        }

        # Check if the test_code is valid and the until the deadline
        test = Test.objects.get(test_code=test_code)

        # If the test's deadline is crossed, don't allow editing
        if datetime.now() > test.deadline or test.sent:
            context['error'] = "You can't edit an old test or one that has been already sent"
            return render(request, 'question.html', context)

        # Check if question exist
        question = Question.objects.filter(test=test, number=num)

        # Check if the new question is available
        # Get the last question
        # If not the num = lastquestion + 1 and not exist: don't allow
        last_question_query = Question.objects.filter(test=test).order_by('-number')

        if not last_question_query:
            last_question = 0
        else:
            last_question = last_question_query[0].number
        
        if not question and num != last_question + 1:
            return redirect(f'/tests/{test_code}/{last_question + 1}')
        

        if question:
            question_name = question[0].name
            options = Option.objects.filter(question=question[0]).order_by('number')

            for option in options:
                if option.correct_answer:
                    option.answer = "T"
                else:
                    option.answer = "F"

                # send option letter a), b), ...
                option.letter = f"{chr(97 + option.number)})"

        if request.method == 'POST':
            question_name = request.POST.get('question')
            question_options = request.POST.getlist('question-option')
            correct_answer_list = request.POST.getlist('correct-answer')

            # Create or update
            obj, __ = Question.objects.update_or_create(test=test, number=num, defaults={'test': test, 'number': num, 'name': question_name})

            # Get all options already created
            for i, option in enumerate(question_options):
                if correct_answer_list[i] == "T":
                    Option.objects.update_or_create(question=obj, number=i, defaults={'question': obj,'number': i, 'option': option, 'correct_answer': True})
                else:
                    Option.objects.update_or_create(question=obj, number=i, defaults={'question': obj, 'number': i, 'option': option, 'correct_answer': False})

            # In case of deleting an option
            # If the options before is higher than the current one, 
            # It means that the user has deleted an option
            if len(options) > len(question_options):
                Option.objects.filter(number__gte=len(question_options)).delete()
            
            return redirect(f'/tests/{test_code}/{num + 1}')

        context['question_options'] = options
        context['question_name'] = question_name
        context['last_question'] = last_question

        return render(request, 'question.html', context)
    except ObjectDoesNotExist:
        print("ERROR 404: Not Found. ObjectDoesNotExist")
        return redirect("/tests/create")

# To make the test available
@login_required
def end_test(request, test_code):
    test = Test.objects.filter(test_code=test_code)

    if not test:
        return HttpResponse('Test not found')

    # At least one question must be done to end a test
    question = Question.objects.filter(test=test[0])

    if not question:
        return HttpResponse('At least one question is necessary to make a test available')
    
    # Check if test_code is available
    if request.method == 'POST':
        test.update(sent=True)
        return redirect('tests:index')
    
    return HttpResponse('An error happend, try it later')

@login_required
def progress_test(request, test_code):
    try:
        test = Test.objects.get(test_code=test_code)
    
        # Get the participants of each text
        results = Participant.objects.filter(test=test, finished=True)

        # to include the answer correct answer to each participant
        participants = map(update_participants_query, results)


        test.deadline -= timedelta(minutes=test.tz)

        context = {
            'test': test,
            'participants': list(participants),
            'user_is_logged': True
        }

        return render(request, 'progress.html', context)
    except:
        print('Ooops, test not found')

        return redirect('tests:index')

@login_required
def delete_test(request, test_code):
    try:
        Test.objects.get(test_code=test_code).delete()
    
        return redirect('tests:index')
    except:
        return redirect('tests:index')
