from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from poll_module.models import Poll, PollOptions, Vote


# Create your views here.
class PollListView(LoginRequiredMixin, ListView):
    model = Poll
    template_name = "poll_module/poll-list.html"
    context_object_name = "polls"


class PollDetailView(LoginRequiredMixin, DetailView):
    model = Poll
    template_name = "poll_module/poll-detail.html"
    context_object_name = "poll"

    def post(self, request: HttpRequest, pk):
        option_id = request.POST.get("option_id")
        option = PollOptions.objects.filter(pk=option_id)
        user = request.user
        old_vote: Vote = Vote.objects.filter(poll_id=self.get_object().id, user_id=user.id).first()
        if old_vote:
            old_vote.delete()
        new_vote = Vote.objects.create(poll_id=self.get_object().id, poll_option_id=option_id, user_id=user.id)
        return JsonResponse({"status": "success"})
