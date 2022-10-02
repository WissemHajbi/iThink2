from django.shortcuts import render, redirect
from django.urls import reverse
from questions.models import question, question_answered, question_comment
from polls.models import user
from django.contrib import messages
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import notification


def answer(request, pk):
    questionn = question.objects.get(id=pk)
    
    print(type(request.user.groups.get(name="staff")))
    
    if questionn.status in ["disapproved", "pending"] and (questionn.creator == str(request.user) or request.user.groups.get(name="staff")):
        print(questionn.question)
        messages.success(request, f"{questionn.status.title()} !")

    if request.method == 'POST':

        

        # this section is for the answering
        if questionn.status == "approved":
            if "disapprove" in request.POST:
                questionn.status = "disapproved"
                questionn.save()
                return redirect('question_answer', pk=questionn.pk)
            
            if "answer" in request.POST:
                useranswer = request.POST["answer"] or "None"
                if useranswer != "None":
                    answered_user = user.objects.get(user=request.user)
                    answered_question = questionn
                    answered_object = question_answered.objects.create(
                        user=answered_user, question=answered_question, answer=useranswer
                    )
                    answered_object.save()
                    return redirect("home", filter_button_pressed="ALL")
                else:
                    messages.success(request, "Please answer the question !")

            # this section is for commenting

            if "comment" in request.POST:
                my_comment = request.POST.getlist("comment") or ""
                if my_comment[0] != "":
                    comment_user = user.objects.get(user=request.user)
                    comment_question = question.objects.get(id=pk)
                    comment_object = question_comment.objects.create(
                        user=comment_user, question=comment_question, comment_str=my_comment[0]
                    )
                    comment_object.save()
                else:
                    messages.success(request, "please write a comment !")

        # this section is for deleting a comment

        if "delete_comment" in request.POST:
            print("")

        # this section is for showing more comments

        if "show_more" in request.POST:
            context = {
                'questions': question
            }
            context["comments"] = question_comment.objects.filter(
                question=question.objects.get(id=pk))
            context["show_more"] = False
            context["show_less"] = True

            return render(request, 'questions/questionAnswer.html', context)

        if "show_less" in request.POST:
            context = {
                'questions': question
            }
            context["comments"] = question_comment.objects.filter(
                question=question.objects.get(id=pk))[:3]
            context["show_more"] = True

            return render(request, 'questions/questionAnswer.html', context)

        
        
    context = {
        "questions": question.objects.get(pk=pk)
    }

    comments = question_comment.objects.filter(
        question=question.objects.get(id=pk))

    if len(comments) > 3:
        context["comments"] = comments[:3]
        context["show_more"] = True
    else:
        context["comments"] = comments
        context["show_more"] = False

    context["comments"] = question_comment.objects.filter(
        question=question.objects.get(id=pk))

    return render(request, "questions/questionAnswer.html", context)


def delete_comment_question(request, id, pk):
    deleted_comment = question_comment.objects.get(id=id)
    if str(deleted_comment.user) == str(request.user):
        deleted_comment.delete()
    else:
        messages.success(
            request, "You can't delete another person's comment !")
    return redirect("question_answer", pk=pk)


class notificationslist(LoginRequiredMixin, ListView):
    model = notification
    template_name = "notification.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["notifications"] = notification.objects.filter(
            user=self.request.user.id).order_by("-notification_date")

        if self.request.method == 'GET':
            if "clear_all" in self.request.GET:
                context["my_notifications"] = notification.objects.filter(
                    user=self.request.user.id
                )
                for notif in context["my_notifications"]:
                    notif.notification_status = "cleared"
                    notif.save()

        return context


class question_suggestion(CreateView):
    model = question
    fields = ["question"]
    template_name = "questions/questionSuggestion.html"

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("home", kwargs={
            "filter_button_pressed": "ALL"})
