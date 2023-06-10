from django import forms

from gallery_module.models import GalleryCategory, GalleryImage, GalleryVideo


class GalleryCategoryForm(forms.ModelForm):
    class Meta:
        model = GalleryCategory
        fields = ['title', 'description']


class GalleryAddImageForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ['title', 'image']
        # widgets = {
        #     'category': forms.Select(attrs={"class": "form-data"})
        # }


class GalleryAddVideoForm(forms.ModelForm):
    class Meta:
        model = GalleryVideo
        fields = ['title', 'video']
