import io
import time

from arabic_reshaper import arabic_reshaper
from bidi.algorithm import get_display
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.images import ImageFile
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from matplotlib import pyplot as plt
from django.db.models.aggregates import Count
from account_module.mixins import JustSuperUser
from contact_module.forms import ContactForm
from contact_module.models import Contact, UnusualContactReason, ContactReport
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
            'contacts': Contact.objects.all(),
            'reports': ContactReport.objects.all(),
        }
        return render(request, 'contact_module/contact-list.html', context)


class ContactTestView(View):
    def get(self, request):
        data = {}
        contacts = UnusualContactReason.objects.annotate(field_count=Count('contact'))
        for contact in contacts:
            test = arabic_reshaper.reshape(u'{0}'.format(contact.field_count))
            test = get_display(test)
            data[contact.title] = test
        # data = {'C': 20, 'C++': 15, 'Java': 30,
        #         'Python': 35}
        courses = list(data.keys())
        values = list(data.values())

        fig = plt.figure(figsize=(10, 5))
        # ax.set_yticklabels([u'é', u'ã', u'â'])
        # creating the bar plot
        plt.bar(courses, values, color='maroon',
                width=0.4)
        xlabel = arabic_reshaper.reshape(u'لیست گرینه ها')
        ylabel = arabic_reshaper.reshape(u'تعداد آرا')
        plt_title = arabic_reshaper.reshape(u'نمودار تعداد رای ها به گزینه ها')
        xlabel = get_display(xlabel)
        ylabel = get_display(ylabel)
        plt_title = get_display(plt_title)
        plt.xlabel(xlabel, fontdict=None, labelpad=None)
        plt.ylabel(ylabel, fontdict=None, labelpad=None)
        plt.title(plt_title, fontdict=None)
        figure = io.BytesIO()
        plt.savefig(figure, format="png")
        time.sleep(2)
        image_file = ImageFile(figure)
        ContactReport.objects.create(image=image_file)
        return HttpResponse("salam kheyli khoobe")
