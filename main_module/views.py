import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView, CreateView

from account_module.models import UserLoggedIn, UserLoggedOut
from main_module.forms import FileAddForm, EventAddForm
from main_module.models import File, Event, Birthday
from news_module.models import News


# Create your views here.
class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        files = File.objects.all()[:8]
        news = News.objects.all()[:8]
        birthdays = Birthday.objects.all()[:8]
        events = Event.objects.all()[:8]
        context = {
            "files": files,
            "news": news,
            "events": events,
            "birthdays": birthdays,
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


class FileAddView(CreateView):
    form_class = FileAddForm
    model = File
    template_name = 'main_module/add-file.html'
    success_url = reverse_lazy('file_list_view')



class LoginReportView(View):
    def get(self, request):
        context = {
            "logins": UserLoggedIn.objects.all()
        }
        return render(request, 'main_module/login-report.html', context)


class LogoutReportView(View):
    def get(self, request):
        context = {
            "logouts": UserLoggedOut.objects.all()
        }
        return render(request, 'main_module/logout-report.html', context)
