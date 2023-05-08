from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView

from news_module.forms import NewsAddForm
from news_module.models import News


# Create your views here.

class NewsListView(LoginRequiredMixin, ListView):
    model = News
    template_name = "news_module/news-list.html"
    context_object_name = "news"


class NewsDetailView(LoginRequiredMixin, DetailView):
    model = News
    template_name = "news_module/news-detail.html"
    context_object_name = "news"


class NewsAddView(View):
    def get(self, request):
        context = {
            "form": NewsAddForm()
        }
        return render(request, 'news_module/add-news.html', context)

    def post(self, request: HttpRequest):
        form = NewsAddForm(request.POST, request.FILES)
        if form.is_valid():
            new = form.save(commit=False)
            new.author = request.user
            new.save()
            return redirect(reverse("news_list_view"))
        context = {
            "form": form
        }
        return render(request, 'news_module/add-news.html', context)
