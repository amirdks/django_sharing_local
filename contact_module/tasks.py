import uuid

from arabic_reshaper import arabic_reshaper
from bidi.algorithm import get_display
from celery import shared_task
from django.db.models import Count
from django.utils import timezone
from matplotlib import pyplot as plt

from contact_module.models import ContactReport, UnusualContactReason


@shared_task
def set_stabled_report():
    data = {}
    # tehran_tz = pytz.timezone('Asia/Tehran')
    now_date = timezone.now()
    yesterday = timezone.datetime(year=now_date.year, month=now_date.month, day=now_date.day, hour=0, minute=0,
                                  second=0, microsecond=0)
    contact_reports = ContactReport.objects.filter(date__gte=yesterday)
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
    instance = ContactReport(image=f"images/plt-{generated_uuid}.png", is_stabled=True)
    instance.save()
    return "success"
