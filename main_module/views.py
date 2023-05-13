import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView, CreateView, DeleteView

from account_module.mixins import JustSuperUser
from account_module.models import UserLoggedIn, UserLoggedOut, User
from main_module.forms import FileAddForm, EventAddForm, BirthdayCreateForm
from main_module.models import File, Event, Birthday
from news_module.models import News


# Create your views here.
class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        files = File.objects.all()[:8]
        news = News.objects.all()[:8]
        birthdays = User.objects.all().order_by("birthday_date")
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


class BirthdayListView(LoginRequiredMixin, View):
    model = Birthday
    template_name = "main_module/birthday-list.html"
    context_object_name = "birthdays"

    def get(self, request):
        users = User.objects.all().order_by("birthday_date")
        context = {
            "birthdays": users
        }
        return render(request, 'main_module/birthday-list.html', context)


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


class FileAddView(JustSuperUser, CreateView):
    form_class = FileAddForm
    model = File
    template_name = 'main_module/add-file.html'
    success_url = reverse_lazy('file_list_view')


class LoginReportView(JustSuperUser, View):
    def get(self, request):
        context = {
            "logins": UserLoggedIn.objects.all()
        }
        return render(request, 'main_module/login-report.html', context)


class LogoutReportView(JustSuperUser, View):
    def get(self, request):
        context = {
            "logouts": UserLoggedOut.objects.all()
        }
        return render(request, 'main_module/logout-report.html', context)


class EventAddView(JustSuperUser, View):
    def get(self, request):
        form = EventAddForm()
        context = {
            'form': form
        }
        return render(request, 'main_module/add-event.html', context)

    def post(self, request):
        print(request.POST)
        # now_time_str = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        # now_time = datetime.datetime.strptime(now_time_str, "%m/%d/%Y %H:%M:%S")
        # end_time_str = end_time.strftime("%m/%d/%Y %H:%M:%S")
        form = EventAddForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            event_date = form.cleaned_data.get("event_date")
            title = form.cleaned_data.get("title")
            Event.objects.create(title=title, event_date=event_date)
            return redirect(reverse("event_list_view"))
        context = {
            'form': form
        }
        return render(request, 'main_module/add-event.html', context)


# class EventCreateView(View):
#     def get(self, request):
#         form = EventAddForm()
class BirthdayAddView(JustSuperUser, View):
    def get(self, request):
        form = BirthdayCreateForm()
        context = {
            'form': form
        }
        return render(request, 'main_module/birthday-create.html', context)

    def post(self, request):
        print(request.POST)
        # now_time_str = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        # now_time = datetime.datetime.strptime(now_time_str, "%m/%d/%Y %H:%M:%S")
        # end_time_str = end_time.strftime("%m/%d/%Y %H:%M:%S")
        form = BirthdayCreateForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            text = form.cleaned_data.get("text")
            user = form.cleaned_data.get("user")
            birthday_date = form.cleaned_data.get("birthday_date")
            Birthday.objects.create(text=text, user=user, birthday_date=birthday_date)
            return redirect(reverse("birthday_list_view"))
        context = {
            'form': form
        }
        return render(request, 'main_module/birthday-create.html', context)


class EventDeleteView(JustSuperUser, DeleteView):
    model = Event
    context_object_name = 'event'
    success_url = reverse_lazy('event_list_view')

    # def form_valid(self, form):
    #     messages.success(self.request, "The task was deleted successfully.")
    #     return super(TaskDelete, self).form_valid(form)


class FileDeleteView(JustSuperUser, DeleteView):
    model = File
    context_object_name = 'file'
    success_url = reverse_lazy('file_list_view')
