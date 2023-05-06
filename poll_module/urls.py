from django.urls import path
from . import views
urlpatterns = [
    path("", views.PollListView.as_view(), name="poll_list_view"),
    path("<int:pk>/", views.PollDetailView.as_view(), name="poll_detail_view"),
]