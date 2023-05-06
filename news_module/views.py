from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, DetailView

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
