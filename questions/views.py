from django.shortcuts import render, redirect
from django.urls import reverse
from questions.models import questions, answered
from polls.models import user
from django.contrib import messages
from django.views.generic import CreateView


def answer(request, pk):
    question = questions.objects.get(id=pk)

    if request.method == 'POST':
        useranswer = request.POST["answer"] or "None"
        if useranswer != "None":
            answered_user = user.objects.get(user=request.user)
            answered_question = questions.objects.get(id=pk)
            answered_object = answered.objects.create(
                user=answered_user, question=answered_question, answer=useranswer
            )
            answered_object.save()
            return redirect("home")
        else:
            messages.success(request, "Please answer the question !")
    context = {
        "questions": question
    }

    return render(request, "questions/questionAnswer.html", context)


class question_suggestion(CreateView):
    model = questions
    fields = ["question"]
