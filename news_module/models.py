from django.db import models


# Create your models here.

class News(models.Model):
    image = models.ImageField(upload_to="images", null=True, blank=True)
    author = models.ForeignKey("account_module.User", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'خبر'
        verbose_name_plural = 'خبر ها'
