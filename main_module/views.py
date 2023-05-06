import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView

from main_module.models import File, Event, Birthday
from news_module.models import News


# Create your views here.
class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        files = File.objects.all()[:5]
        news = News.objects.all()[:5]
        events = Event.objects.all()[:5]
        context = {
            "files": files,
            "news": news,
            "events": events,
        }
        return render(request, "main_module/home.html", context)


class EventListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = "main_module/event-list.html"
    context_object_name = "events"


class BirthdayListView(LoginRequiredMixin, ListView):
    model = Birthday
    template_name = "main_module/birthday-list.html"
    context_object_name = "birthdays"


class FileListView(LoginRequiredMixin, ListView):
    model = File
    template_name = "main_module/file-list.html"
    context_object_name = "files"


class EventDetailView(LoginRequiredMixin, DetailView):
    model = Event
    template_name = "main_module/event-detail.html"
    context_object_name = "event"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = context.get("event")
        reaming_date = datetime.datetime.today().date() - event.event_date
        days = reaming_date.days
        context["reaming_date"] = reaming_date
        context["reaming_days"] = days
        return context


class BirthdayDetailView(LoginRequiredMixin, DetailView):
    model = Birthday
    template_name = "main_module/birthday-detail.html"
    context_object_name = "birthday"


class TestView(TemplateView):
    template_name = 'shared/__layout.html'
