from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home_view"),
    path("test/", views.TestView.as_view(), name="test_view"),
    path("events/", views.EventListView.as_view(), name="event_list_view"),
    path("events/<int:pk>/", views.EventDetailView.as_view(), name="event_detail_view"),
    path("birthdays/", views.BirthdayListView.as_view(), name="birthday_list_view"),
    path("birthdays/<int:pk>/", views.BirthdayDetailView.as_view(), name="birthday_detail_view"),
    path("files/", views.FileListView.as_view(), name="file_list_view"),
    path("files/", views.FileListView.as_view(), name="file_list_view"),
]
