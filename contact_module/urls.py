from django.urls import path
from . import views

urlpatterns = [
    path('list/<int:form_id>', views.ContactListView.as_view(), name="contact_list_view"),
    path('user-form-list/', views.ContactUserFormList.as_view(), name="contact_user_form_list_view"),
    path('form-list/', views.ContactFormListView.as_view(), name="contact_form_list_view"),
    path('form-list/<int:form_id>/change/', views.ContactFormChangeView.as_view(), name="contact_form_change_view"),
    path('form-list/add/', views.ContactFormModelCreate.as_view(), name="contact_form_create_view"),
    path('form-list/delete/<int:pk>/', views.ContactFormDeleteView.as_view(), name='contact_form_delete_view'),
    path('get-today/<int:form_id>/', views.ContactGetReport.as_view(), name='add_new_contact_report'),
    path('<int:form_id>/', views.ContactCreateView.as_view(), name="contact_view"),
]
