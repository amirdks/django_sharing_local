from django.urls import path
from . import views

urlpatterns = [
    path("", views.GalleryCategoryListView.as_view(), name='gallery_category_list_view'),
    path("add/", views.GalleryAddView.as_view(), name='gallery_category_add'),
    path("<int:category_id>/", views.GalleryListView.as_view(), name='gallery_list_view'),
    path("<int:category_id>/add-image/", views.GalleryAddImageView.as_view(), name='gallery_add_image'),
    path("<int:category_id>/add-video/", views.GalleryAddVideoView.as_view(), name='gallery_add_video'),

]
