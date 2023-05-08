from django.db import models


# Create your models here.

class Poll(models.Model):
    owner = models.ForeignKey("account_module.User", on_delete=models.CASCADE)
    question = models.CharField(
        max_length=30,
        verbose_name='عنوان سوال',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='زمان ساخت',
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='فعال / غیرفعال',
    )

    class Meta:
        verbose_name = 'نظرسنجی'
        verbose_name_plural = 'نظرسنجی ها'
        ordering = ('-created_at',)

    # Methods
    def __str__(self):
        return self.question

    @property
    def all_count(self):
        polls = self.vote_set.count()
        return polls


class PollOptions(models.Model):
    poll = models.ForeignKey(
        Poll,
        on_delete=models.CASCADE,
        related_name='poll_option',
        verbose_name='برای نظرسنجی',
    )
    option = models.CharField(
        max_length=30,
        verbose_name='گزینه',
    )
    option_count = models.IntegerField(
        default=0,
        verbose_name='شمارش گزینه',
    )

    # Metadata
    class Meta:
        verbose_name = 'گزینه'
        verbose_name_plural = 'گزینه ها'

    # Methods
    def __str__(self):
        return self.option

    def option_count_x(self):
        count = 0
        for vote in self.vote_set.all():
            count += 1
        return count

    def poll_percent(self):
        try:
            percent = round(self.vote_set.count() * 100 / self.poll.all_count)
        except ZeroDivisionError:
            percent = 0
        return percent


class Vote(models.Model):
    user = models.ForeignKey("account_module.User", on_delete=models.CASCADE)
    poll = models.ForeignKey("Poll", on_delete=models.CASCADE)
    poll_option = models.ForeignKey("PollOptions", on_delete=models.CASCADE)
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='زمان ساخت',
    )

    class Meta:
        verbose_name = 'رای'
        verbose_name_plural = 'رای ها'

    # Methods
    def __str__(self):
        return self.user.email
