from django.db import models


# Create your models here.

class GalleryCategory(models.Model):
    title = models.CharField(max_length=255, verbose_name='عنوان دسته بندی')
    description = models.TextField(verbose_name='توضبحات')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی گالری'
        verbose_name_plural = 'دسته بندی های گالری'


class GalleryImage(models.Model):
    category = models.ForeignKey("GalleryCategory", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/gallery")
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


class GalleryVideo(models.Model):
    category = models.ForeignKey("GalleryCategory", on_delete=models.CASCADE)
    video = models.FileField(upload_to="video/gallery")
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
