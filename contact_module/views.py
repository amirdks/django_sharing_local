from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from account_module.mixins import JustSuperUser
from contact_module.forms import ContactForm
from contact_module.models import Contact
from utils.form_errors import form_error


# Create your views here.
class ContactCreateView(LoginRequiredMixin, View):
    def get(self, request):
        context = {
            "form": ContactForm()
        }
        return render(request, 'contact_module/contact-form.html', context)

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            agent = form.cleaned_data.get("agent")
            phone_number = form.cleaned_data.get("phone_number")
            unusual_contact_reason = form.cleaned_data.get("unusual_contact_reason")
            description = form.cleaned_data.get("description")
            new_contact = Contact.objects.create(sender_id=request.user.id, agent=agent, phone_number=phone_number,
                                                 unusual_contact_reason_id=unusual_contact_reason.id,
                                                 description=description)
            return redirect(reverse("home_view"))
        context = {
            "form": form
        }
        return render(request, 'contact_module/contact-form.html', context)


class ContactListView(JustSuperUser, View):
    def get(self, request):
        context = {
            'contacts': Contact.objects.all()
        }
        return render(request, 'contact_module/contact-list.html', context)
