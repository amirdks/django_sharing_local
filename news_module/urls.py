from django.urls import path
from . import views

urlpatterns = [
    path("", views.NewsListView.as_view(), name="news_list_view"),
    path("add/", views.NewsAddView.as_view(), name="news_add_view"),
    path("<int:pk>/", views.NewsDetailView.as_view(), name="news_detail_view"),
    path('delete/<int:pk>/', views.NewsDeleteView.as_view(), name='news_delete_view'),
]
