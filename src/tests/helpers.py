from participants.models import Participant, Participant_answer
from .models import Question, Option

# To include for each question answered by the participant, the correct one 
def update_participants_query(participant):
    test = participant.test
    questions = Question.objects.filter(test=test)
    
    for question in questions:
        correct_answer = Option.objects.get(question=question, correct_answer=True).number
        participant_answer = Participant_answer.objects.get(participant=participant, question=question).answer.number

        # to convert the number to a letter
        question.correct_answer = f"{chr(97 + correct_answer)})"
        question.participant_answer = f"{chr(97 + participant_answer)})"
        
    participant.questions = questions
        

    return participant