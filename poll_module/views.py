from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.views import View
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_vote"] = Vote.objects.filter(user_id=self.request.user.id, poll_id=context["poll"].id).first()
        print(context)
        return context

    def post(self, request: HttpRequest, pk):
        option_id = request.POST.get("option_id")
        option = PollOptions.objects.filter(pk=option_id).first()
        print(option)
        user = request.user
        old_vote: Vote = Vote.objects.filter(poll_id=self.get_object().id, user_id=user.id).first()
        if old_vote:
            option.option_count -= 1
            old_vote.delete()
        option.option_count += 1
        option.save()
        new_vote = Vote.objects.create(poll_id=self.get_object().id, poll_option_id=option_id, user_id=user.id)
        request.user.vote_set.all()
        return JsonResponse({"status": "success", "message": "رای شما با موفقیت ثبت شد"})


class DeleteVoteView(View):
    http_method_names = ["post"]

    def post(self, request):
        vote_id = request.POST.get("vote_id")
        vote = Vote.objects.filter(pk=vote_id).first()
        if vote:
            vote.delete()
            return JsonResponse({"status": "success", "message": "رای شما با موفقیت حذف شد"})
        return JsonResponse({"status": "error", "message": "رای مورد نظر شما یافت نشد"})
