from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView

from account_module.mixins import JustSuperUser
from gallery_module.forms import GalleryCategoryForm, GalleryAddImageForm, GalleryAddVideoForm
from gallery_module.models import GalleryCategory


# Create your views here.
class GalleryCategoryListView(LoginRequiredMixin, ListView):
    model = GalleryCategory
    template_name = 'gallery_module/gallery_category_list.html'
    context_object_name = 'gallerycategories'
    ordering = ["-created_at"]


class GalleryListView(LoginRequiredMixin, View):
    def get(self, request, category_id):
        gallery_category = get_object_or_404(GalleryCategory, pk=category_id)
        context = {
            'gallery_category': gallery_category
        }
        return render(request, 'gallery_module/gallery_list.html', context)


class GalleryAddView(JustSuperUser, View):
    def get(self, request):
        form = GalleryCategoryForm()
        context = {
            "form": form
        }
        return render(request, 'gallery_module/gallery_category_add.html', context)

    def post(self, request):
        form = GalleryCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("gallery_category_list_view"))
        context = {
            "form": form
        }
        return render(request, 'gallery_module/gallery_category_add.html', context)


class GalleryAddImageView(JustSuperUser, View):
    def get(self, request, category_id):
        form = GalleryAddImageForm()
        gallery_category = get_object_or_404(GalleryCategory, pk=category_id)
        context = {
            "form": form,
            'gallery_category': gallery_category
        }
        return render(request, 'gallery_module/gallery_add_image.html', context)

    def post(self, request, category_id):
        form = GalleryAddImageForm(request.POST, request.FILES)
        gallery_category = get_object_or_404(GalleryCategory, pk=category_id)
        if form.is_valid():
            new_image = form.save(commit=False)
            new_image.category = gallery_category
            new_image.save()
            return redirect(reverse("gallery_list_view", kwargs={"category_id": category_id}))
        context = {
            "form": form,
            'gallery_category': gallery_category
        }
        return render(request, 'gallery_module/gallery_add_image.html', context)


class GalleryAddVideoView(JustSuperUser, View):
    def get(self, request, category_id):
        form = GalleryAddVideoForm()
        gallery_category = get_object_or_404(GalleryCategory, pk=category_id)
        context = {
            "form": form,
            'gallery_category': gallery_category
        }
        return render(request, 'gallery_module/gallery_add_video.html', context)

    def post(self, request, category_id):
        form = GalleryAddVideoForm(request.POST, request.FILES)
        gallery_category = get_object_or_404(GalleryCategory, pk=category_id)
        if form.is_valid():
            new_image = form.save(commit=False)
            new_image.category = gallery_category
            new_image.save()
            return redirect(reverse("gallery_list_view", kwargs={"category_id": category_id}))
        context = {
            "form": form,
            'gallery_category': gallery_category
        }
        return render(request, 'gallery_module/gallery_add_video.html', context)
