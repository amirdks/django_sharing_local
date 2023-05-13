from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home_view"),
    path("test/", views.TestView.as_view(), name="test_view"),
    path("events/", views.EventListView.as_view(), name="event_list_view"),
    path("events/<int:pk>/", views.EventDetailView.as_view(), name="event_detail_view"),
    path('events/delete/<int:pk>/', views.EventDeleteView.as_view(), name='event_delete_view'),
    path("events/add/", views.EventAddView.as_view(), name="event_add_view"),
    path("birthdays/", views.BirthdayListView.as_view(), name="birthday_list_view"),
    path("birthdays/add/", views.BirthdayAddView.as_view(), name="birthday_add_view"),
    path("birthdays/<int:pk>/", views.BirthdayDetailView.as_view(), name="birthday_detail_view"),
    path("files/", views.FileListView.as_view(), name="file_list_view"),
    path("files/add/", views.FileAddView.as_view(), name="file_add_view"),
    path('files/delete/<int:pk>/', views.FileDeleteView.as_view(), name='file_delete_view'),
    path("login-report", views.LoginReportView.as_view(), name="login_report_view"),
    path("logout-report", views.LogoutReportView.as_view(), name="logout_report_view"),
]
