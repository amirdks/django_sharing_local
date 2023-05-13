from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login_view"),
    path("logout/", views.LogoutView.as_view(), name="logout_view"),
    path("call-log/", views.CallLogView.as_view(), name="call_log_view"),
    path("user-list/", views.UserListView.as_view(), name="user_list_view"),
    path("user-list/add/", views.UserCreateView.as_view(), name="user_add_view"),
    path("user-list/<int:pk>/edit/", views.UserEditView.as_view(), name="user_edit_view"),
    path("user-list/<int:pk>/delete/", views.UserDeleteView.as_view(), name="user_delete_view"),
]
