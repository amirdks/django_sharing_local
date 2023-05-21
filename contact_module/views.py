import datetime
import io
import time
import uuid

from PIL.ImageFile import ImageFile
from arabic_reshaper import arabic_reshaper
from bidi.algorithm import get_display
from dateutil import tz
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files import File
from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
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


class ContactGetReport(JustSuperUser, View):
    def get(self, request):
        data = {}
        now_date = timezone.now()
        yesterday = timezone.datetime(year=now_date.year, month=now_date.month, day=now_date.day, hour=0, minute=0,
                                      second=0, microsecond=0)
        contacts = UnusualContactReason.objects.annotate(field_count=Count('contact')).filter(
            contact__created_at__lt=yesterday)
        if not contacts:
            return HttpResponse("امروز هیچ ارتباطی توسط کارمندان ثبت نشده است")
        for contact in contacts:
            data[contact.title] = contact.field_count
        courses = list(data.keys())
        values = list(data.values())

        fig = plt.figure(figsize=(10, 5))
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
        # figure = io.BytesIO()
        generated_uuid = uuid.uuid4()
        plt_file_name = f'media/images/plt-{generated_uuid}.png'
        plt.savefig(plt_file_name, format='png')
        instance = ContactReport(image=f"images/plt-{generated_uuid}.png")
        instance.save()
        return redirect(reverse("contact_list_view"))
