from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.ContactListView.as_view(), name="contact_list_view"),
    path('', views.ContactCreateView.as_view(), name="contact_view"),
    path('get-today/', views.ContactGetReport.as_view(), name='add_new_contact_report'),
]