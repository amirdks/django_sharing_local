from django.contrib import admin

from gallery_module.models import GalleryVideo, GalleryCategory, GalleryImage

# Register your models here.
admin.site.register(GalleryImage)
admin.site.register(GalleryVideo)
admin.site.register(GalleryCategory)
