from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import poll, deleted, voted, user, poll_comment
from questions.models import question, question_answered
from django.contrib.auth.models import User
from .forms import registerForm
from django.contrib.auth import login, authenticate
import random
from django.http import QueryDict


class pollslist(LoginRequiredMixin, ListView):
    model = poll
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["questions"] = question.objects.all()
        context["answered"] = question_answered.objects.all()
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
                    # print(f"{questionitem.question} = {answereditem.user.user.username} = {self.request.user.id}")
                    questions_not_wanted_id.append(quesitionitem.id)

            if questionitem.status == "disapproved":
                # print(questionitem.question)
                questions_not_wanted_id.append(questionitem.id)

        questions_wanted_id = []
        for id in questions_all_id:
            if id not in questions_not_wanted_id:
                questions_wanted_id.append(id)

        context["questions"] = question.objects.filter(
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
                    # print(f"deleted = {deleteditem.user.username} {deleteditem.user.user.id} {self.request.user.id}")
                    polls_not_wanted_id.append(pollitem.id)

            for voteditem in context["voted"]:
                if pollitem.id == voteditem.poll.id and voteditem.user.user.id == self.request.user.id:
                    # print(f"voted = {voteditem.user.username} {voteditem.user.user.id} {self.request.user.id}")
                    polls_not_wanted_id.append(pollitem.id)

            if pollitem.status == "disapproved":
                # print(pollitem.question)
                polls_not_wanted_id.append(pollitem.id)

        polls_wanted_id = []
        for id in polls_all_id:
            if id not in polls_not_wanted_id:
                polls_wanted_id.append(id)

        random.shuffle(polls_wanted_id)

        polls = poll.objects.filter(id__in=polls_wanted_id)

        context["polls"] = polls

        if self.kwargs["filter_button_pressed"] == "ALL":
            context["polls"] = poll.objects.all()
            context["polls"] = poll.objects.filter(
                id__in=polls_wanted_id)[:6]
            context["filter_button_pressed"] = "ALL"

        elif self.kwargs["filter_button_pressed"] == "Sports":
            context["polls"] = context["polls"].filter(genre="s")[:6]
            context["filter_button_pressed"] = "Sports"

        elif self.kwargs["filter_button_pressed"] == "Politics":
            context["polls"] = context["polls"].filter(genre="p")[:6]
            context["filter_button_pressed"] = "Politics"

        elif self.kwargs["filter_button_pressed"] == "Gaming":
            context["polls"] = context["polls"].filter(genre="g")[:6]
            context["filter_button_pressed"] = "Gaming"

        elif self.kwargs["filter_button_pressed"] == "Music":
            context["polls"] = context["polls"].filter(genre="m")[:6]
            context["filter_button_pressed"] = "Music"

        elif self.kwargs["filter_button_pressed"] == "Health":
            context["polls"] = context["polls"].filter(genre="h")[:6]
            context["filter_button_pressed"] = "Health"

        return context


class profileView(LoginRequiredMixin, ListView):
    model = user
    template_name = "profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = user.objects.get(username=self.kwargs["name"])
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

        answered_questions_number = question_answered.objects.filter(
            user=context["user"].id)
        context["answered_questions_number"] = len(answered_questions_number)

        context["owned_polls"] = poll.objects.filter(
            creator=self.kwargs["name"])

        context["owned_questions"] = question.objects.filter(
            creator=self.kwargs["name"])

        # continue here working on sending the poll creator to this class
        # print(self.request.GET.getlist("poll_creator") or [""])
        return context


class loginView(LoginView):
    template_name = "login.html"
    fields = "__all__"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("home", kwargs={"filter_button_pressed": "ALL"})


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
            user_gender = request.POST.getlist("gender")
            user_profile_picture_number = request.POST.getlist(
                "profile_picture_number")
            user_cover_picture_number = random.randint(0, 7)
            user_object = user.objects.create(
                user=User_object, gender=user_gender, username=username, email=email, profile_picture_number=user_profile_picture_number, cover_picture_number=user_cover_picture_number)
            user_object.save()

            return redirect("login")

    else:
        form = registerForm()
    context['registerForm'] = form
    return render(request, "register.html", context)


def vote(request, pk):
    polll = poll.objects.get(id=pk)

    if request.method == 'POST':

        # this section is for the voting

        if "vote" in request.POST:
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
                return redirect("home", filter_button_pressed="ALL")
            else:
                messages.success(request, "Please choose an answer !")

        # this section is for commenting

        if "comment" in request.POST:
            my_comment = request.POST.getlist("comment") or ""
            if my_comment != "":
                comment_user = user.objects.get(user=request.user)
                comment_poll = poll.objects.get(id=pk)
                comment_object = poll_comment.objects.create(
                    user=comment_user, poll=comment_poll, comment_str=my_comment[0]
                )
                comment_object.save()
            else:
                messages.success(request, "Please write a comment !")

            # deleting the comment from the QueryDict to not comment again
            
            request.POST._mutable = True
            del request.POST["comment"]
            request.POST._mutable = False

        # this section is for showing more comments

        if "show_more" in request.POST:
            context = {
                'polls': polll
            }
            context["comments"] = poll_comment.objects.filter(
                poll=poll.objects.get(id=pk))
            context["show_more"] = False
            context["show_less"] = True

            return render(request, 'polls/pollVote.html', context)

        if "show_less" in request.POST:
            context = {
                'polls': polll
            }
            context["comments"] = poll_comment.objects.filter(
                poll=poll.objects.get(id=pk))[:3]
            context["show_more"] = True

            return render(request, 'polls/pollVote.html', context)

    context = {
        'polls': polll
    }

    comments = poll_comment.objects.filter(
        poll=poll.objects.get(id=pk))

    if len(comments) > 3:
        context["comments"] = comments[:3]
        context["show_more"] = True
    else:
        context["comments"] = comments
        context["show_more"] = False

    # this section is searching for the highest voted choice to  highlight it after

    voted_polls = voted.objects.filter(poll=187)

    choices = {
        "1": 0,
        "2": 1,
        "3": 0,
        "4": 0,
        "5": 0,
        "6": 0,
    }

    for i in voted_polls:
        choices[str(i.choice)] += 1

    context["max_choice"] = int(max(choices, key=choices.get))

    return render(request, 'polls/pollVote.html', context)


def delete(request, pk, filter_button_pressed):

    # filter_button_pressed to return at the same filtred button before the delete

    deleted_user = user.objects.get(user=request.user)
    deleted_poll = poll.objects.get(id=pk)
    deleted_object = deleted.objects.create(
        user=deleted_user, poll=deleted_poll)
    deleted_object.save()

    return redirect("home", filter_button_pressed=filter_button_pressed)


def delete_comment_poll(request, id, pk):
    deleted_comment = poll_comment.objects.get(id=id)
    if str(deleted_comment.user) == str(request.user):
        deleted_comment.delete()
    else:
        messages.success(
            request, "You can't delete another person's comment !")
    return redirect("poll_vote", pk=pk)


class poll_suggestion(CreateView):
    model = poll
    fields = ["question", "genre", "answer1", "answer2",
              "answer3", "answer4", "answer5", "answer6"]
    template_name = "polls/pollSuggestion.html"

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return redirect("home", filter_button_pressed="ALL")
