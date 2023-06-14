import datetime
import io
import time
import uuid

import pytz as pytz
from PIL.ImageFile import ImageFile
from arabic_reshaper import arabic_reshaper
from bidi.algorithm import get_display
from dateutil import tz
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files import File
from django.core.files.base import ContentFile
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import DeleteView
from matplotlib import pyplot as plt
from django.db.models.aggregates import Count
from account_module.mixins import JustSuperUser
from contact_module.forms import ContactForm, ContactFormModelForm
from contact_module.models import Contact, UnusualContactReason, ContactReport, ContactFormModel
from utils.form_errors import form_error


# Create your views here.
# TODO : check user access to form
class ContactCreateView(LoginRequiredMixin, View):
    def get(self, request, form_id):
        form = ContactForm()
        current_form = get_object_or_404(ContactFormModel, pk=form_id)
        form.fields["head_administrative_department"].queryset = form.fields[
            "head_administrative_department"].queryset.filter(
            administrative_department__in=request.user.administrative_department.all())
        form.fields["unusual_contact_reason"].queryset = current_form.unusual_contact_reason.all()
        context = {
            "form": form,
            "current_form": current_form,
        }
        return render(request, 'contact_module/contact-form.html', context)

    def post(self, request, form_id):
        form = ContactForm(request.POST)
        current_form = get_object_or_404(ContactFormModel, pk=form_id)
        if form.is_valid():
            phone_number = form.cleaned_data.get("phone_number")
            unusual_contact_reason = form.cleaned_data.get("unusual_contact_reason")
            description = form.cleaned_data.get("description")
            head_administrative_department = form.cleaned_data.get("head_administrative_department")
            new_contact = Contact.objects.create(sender_id=request.user.id, form=current_form,
                                                 phone_number=phone_number,
                                                 unusual_contact_reason_id=unusual_contact_reason.id,
                                                 description=description,
                                                 head_administrative_department=head_administrative_department)
            data = {}
            # tehran_tz = pytz.timezone('Asia/Tehran')
            now_date = timezone.now()
            yesterday = timezone.datetime(year=now_date.year, month=now_date.month, day=now_date.day, hour=0, minute=0,
                                          second=0, microsecond=0)
            contact_reports = ContactReport.objects.filter(date__gte=yesterday, is_stabled=False)
            if contact_reports:
                contact_reports.delete()

            contacts_reasons_match = UnusualContactReason.objects.annotate(field_count=Count('contact')).filter(
                contact__created_at__gte=yesterday)

            contact_reasons = UnusualContactReason.objects.filter(is_active=True)
            for reason in contact_reasons:
                data[reason.title] = 0
            for contacts_reason_match in contacts_reasons_match:
                data[contacts_reason_match.title] = contacts_reason_match.field_count
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
            return redirect(reverse("home_view"))
        context = {
            "form": form,
            "current_form": current_form,
        }
        return render(request, 'contact_module/contact-form.html', context)


class ContactListView(JustSuperUser, View):
    def get(self, request: HttpRequest, form_id):
        contacts = Contact.objects.filter(form_id=form_id)
        current_form = get_object_or_404(ContactFormModel, pk=form_id)
        reports = ContactReport.objects.all()
        if not request.user.is_superuser and request.user.administrative_department_head.exists():
            contacts = contacts.filter(
                head_administrative_department__in=request.user.administrative_department_head.all())
            reports = reports
        context = {
            'contacts': contacts,
            'reports': reports,
            "current_form": current_form
        }
        return render(request, 'contact_module/contact-list.html', context)


class ContactGetReport(JustSuperUser, View):
    def get(self, request, form_id):
        data = {}
        current_form = get_object_or_404(ContactFormModel, pk=form_id)
        now_date = timezone.now()
        yesterday = timezone.datetime(year=now_date.year, month=now_date.month, day=now_date.day, hour=0, minute=0,
                                      second=0, microsecond=0)
        contacts = UnusualContactReason.objects.annotate(field_count=Count('contact')).filter(
            contact__created_at__lt=yesterday, contact__form_id=current_form.pk)
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
        return redirect(reverse("contact_list_view", kwargs={"form_id": current_form.pk}))


class ContactFormListView(JustSuperUser, View):
    def get(self, request):
        forms = ContactFormModel.objects.all()
        context = {
            'forms': forms
        }
        return render(request, 'contact_module/form_list.html', context)


class ContactFormDeleteView(JustSuperUser, DeleteView):
    model = ContactFormModel
    context_object_name = 'form_obj'
    template_name = 'contact_module/form_confirm_delete.html'
    success_url = reverse_lazy('contact_form_list_view')


class ContactFormModelCreate(JustSuperUser, View):
    def get(self, request):
        form = ContactFormModelForm()
        context = {
            'form': form,
        }
        return render(request, 'contact_module/form_add.html', context)

    def post(self, request):
        form = ContactFormModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("contact_form_list_view"))
        context = {
            'form': form,
        }
        return render(request, 'contact_module/form_add.html', context)


class ContactUserFormList(LoginRequiredMixin, View):
    def get(self, request: HttpRequest):
        # forms = ContactFormModel.objects.filter(users__in=request.user)
        forms = request.user.contactformmodel_set.all()
        context = {
            'forms': forms
        }
        return render(request, 'contact_module/user_form_list.html', context)


class ContactFormChangeView(JustSuperUser, View):
    def get(self, request, form_id):
        current_form = get_object_or_404(ContactFormModel, pk=form_id)
        form = ContactFormModelForm(instance=current_form)
        context = {
            "form": form,
            "current_form": current_form,
        }
        return render(request, 'contact_module/form_change.html', context)

    def post(self, request, form_id):
        current_form = get_object_or_404(ContactFormModel, pk=form_id)
        form = ContactFormModelForm(request.POST, instance=current_form)
        if form.is_valid():
            form.save()
            return redirect(reverse("contact_form_list_view"))
        context = {
            "form": form,
            "current_form": current_form,
        }
        return render(request, 'contact_module/form_change.html', context)
