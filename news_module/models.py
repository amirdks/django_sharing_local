from django.db import models


# Create your models here.

class News(models.Model):
    author = models.ForeignKey("account_module.User", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)
