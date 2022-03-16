from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.list import ListView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import poll, deleted, voted, user
from questions.models import questions, answered
from django.contrib.auth.models import User
from .forms import registerForm
from django.contrib.auth import login, authenticate


class pollslist(LoginRequiredMixin, ListView):
    model = poll
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["questions"] = questions.objects.all()
        context["answered"] = answered.objects.all()
        context["polls"] = poll.objects.all()
        context["voted"] = voted.objects.all()
        context["deleted"] = deleted.objects.all()

        """
            this part is filtering (by id) the questions that are not answered by the user
        """

        questions_all_id = []
        for questionitem in context["questions"]:
            questions_all_id.append(questionitem.id)

        questions_not_wanted_id = []
        for quesitionitem in context["questions"]:

            for answereditem in context["answered"]:
                if quesitionitem.id == answereditem.question.id and answereditem.user.user.id == self.request.user.id:
                    #print(f"question = {answereditem.user.username} {answereditem.user.user.id} {self.request.user.id}")
                    questions_not_wanted_id.append(quesitionitem.id)

        questions_wanted_id = []
        for id in questions_all_id:
            if id not in questions_not_wanted_id:
                questions_wanted_id.append(id)

        context["questions"] = questions.objects.filter(
            id__in=questions_wanted_id)

        """
            this part is filtering (by id) the polls that are neither voted on or deleted by the user
        """

        polls_all_id = []
        for pollitem in context["polls"]:
            polls_all_id.append(pollitem.id)

        polls_not_wanted_id = []
        for pollitem in context["polls"]:

            for deleteditem in context["deleted"]:
                if pollitem.id == deleteditem.poll.id and deleteditem.user.user.id == self.request.user.id:
                    #print(f"deleted = {deleteditem.user.username} {deleteditem.user.user.id} {self.request.user.id}")
                    polls_not_wanted_id.append(pollitem.id)

            for voteditem in context["voted"]:
                if pollitem.id == voteditem.poll.id and voteditem.user.user.id == self.request.user.id:
                    #print(f"voted = {voteditem.user.username} {voteditem.user.user.id} {self.request.user.id}")
                    polls_not_wanted_id.append(pollitem.id)

        polls_wanted_id = []
        for id in polls_all_id:
            if id not in polls_not_wanted_id:
                polls_wanted_id.append(id)
        

        context["polls"] = poll.objects.filter(id__in=polls_wanted_id)

        filter_button = []

        if self.request.method == "GET":

            if not filter_button:
                filter_button = self.request.GET.getlist(
                    "filter_button") or ['']

            if filter_button[0] == "Sports":
                context["polls"] = context["polls"].filter(genre="s")[:6]
                context["filter_button_pressed"] = "Sports"
            elif filter_button[0] == "Politics":
                context["polls"] = context["polls"].filter(genre="p")[:6]
                context["filter_button_pressed"] = "Politics"
            elif filter_button[0] == "Gaming":
                context["polls"] = context["polls"].filter(genre="g")[:6]
                context["filter_button_pressed"] = "Gaming"
            elif filter_button[0] == "Music":
                context["polls"] = context["polls"].filter(genre="m")[:6]
                context["filter_button_pressed"] = "Music"
            elif filter_button[0] == "Health":
                context["polls"] = context["polls"].filter(genre="h")[:6]
                context["filter_button_pressed"] = "Health"
            else:
                context["polls"] = poll.objects.all()
                context["polls"] = poll.objects.filter(
                    id__in=polls_wanted_id)[:6]
                context["filter_button_pressed"] = "ALL"

        return context


class profileView(LoginRequiredMixin, ListView):
    model = user
    template_name = "profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = user.objects.get(user=self.request.user)
        voted_polls = voted.objects.filter(user=context["user"].id)
        context["voted_polls_number"] = len(voted_polls)

        context["sports"] = 0
        context["politics"] = 0
        context["gaming"] = 0
        context["music"] = 0
        context["health"] = 0
        for vote in voted_polls:
            if vote.poll.genre == "s":
                context["sports"] += 1
            elif vote.poll.genre == "p":
                context["politics"] += 1
            elif vote.poll.genre == "g":
                context["gaming"] += 1
            elif vote.poll.genre == "m":
                context["music"] += 1
            elif vote.poll.genre == "h":
                context["health"] += 1

        answered_questions_number = answered.objects.filter(
            user=context["user"].id)
        context["answered_questions_number"] = len(answered_questions_number)

        return context


class loginView(LoginView):
    template_name = "login.html"
    fields = "__all__"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("home")


def register_view(request, *args, **kwargs):
    user_ob = request.user
    if user_ob.is_authenticated:
        return HttpResponse(f"you are already athenticated as {user.email}")

    context = {}
    if request.method == "POST":
        form = registerForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            User_object = User.objects.get(username=username)
            email = form.cleaned_data.get('email')
            user_object = user.objects.create(
                user=User_object, username=username, email=email)
            user_object.save()
            return redirect("login")
    else:
        form = registerForm()
    context['registerForm'] = form
    return render(request, "register.html", context)


def vote(request, pk):
    polll = poll.objects.get(id=pk)

    if request.method == 'POST':
        answer = request.POST.getlist("answer") or ('None')
        if answer != "None":
            if answer[0] == "answer1":
                polll.count1 += 1
                voted_user = user.objects.get(user=request.user)
                voted_poll = poll.objects.get(id=pk)
                voted_choice = 1
                voted_object = voted.objects.create(
                    user=voted_user, poll=voted_poll, choice=voted_choice)
                voted_object.save()
            elif answer[0] == "answer2":
                polll.count2 += 1
                voted_user = user.objects.get(user=request.user)
                voted_poll = poll.objects.get(id=pk)
                voted_choice = 2
                voted_object = voted.objects.create(
                    user=voted_user, poll=voted_poll, choice=voted_choice)
                voted_object.save()
            elif answer[0] == "answer3":
                polll.count3 += 1
                voted_user = user.objects.get(user=request.user)
                voted_poll = poll.objects.get(id=pk)
                voted_choice = 3
                voted_object = voted.objects.create(
                    user=voted_user, poll=voted_poll, choice=voted_choice)
                voted_object.save()
            elif answer[0] == "answer4":
                polll.count4 += 1
                voted_user = user.objects.get(user=request.user)
                voted_poll = poll.objects.get(id=pk)
                voted_choice = 4
                voted_object = voted.objects.create(
                    user=voted_user, poll=voted_poll, choice=voted_choice)
                voted_object.save()
            elif answer[0] == "answer5":
                polll.count5 += 1
                voted_user = user.objects.get(user=request.user)
                voted_poll = poll.objects.get(id=pk)
                voted_choice = 5
                voted_object = voted.objects.create(
                    user=voted_user, poll=voted_poll, choice=voted_choice)
                voted_object.save()
            elif answer[0] == "answer6":
                polll.count6 += 1
                voted_user = user.objects.get(user=request.user)
                voted_poll = poll.objects.get(id=pk)
                voted_choice = 6
                voted_object = voted.objects.create(
                    user=voted_user, poll=voted_poll, choice=voted_choice)
                voted_object.save()
            else:
                return reverse("poll_vote", kwargs={
                    "pk": pk
                })

            polll.save()
            return redirect("home")
        else:
            messages.success(request, "Please choose an answer !")
    context = {
        'polls': polll
    }
    return render(request, 'polls/pollVote.html', context)


def delete(request, pk, filter_button_pressed):
    deleted_user = user.objects.get(user=request.user)
    deleted_poll = poll.objects.get(id=pk)
    deleted_object = deleted.objects.create(
        user=deleted_user, poll=deleted_poll)
    deleted_object.save()

    return redirect("home")
