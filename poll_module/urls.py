from django.urls import path
from . import views
urlpatterns = [
    path("", views.PollListView.as_view(), name="poll_list_view"),
    path("delete-vote/", views.DeleteVoteView.as_view(), name="delete_vote_view"),
    path("<int:pk>/", views.PollDetailView.as_view(), name="poll_detail_view"),
    path("add/", views.PollAddView.as_view(), name="poll_add_view"),
    path('delete/<int:pk>/', views.PollDeleteView.as_view(), name='poll_delete_view'),
]