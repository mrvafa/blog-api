from django.urls import path

from .view import (TagListAPIView, TagDetailAPIView, TagUpdateAPIView, TagDestroyAPIView, TagCreateAPIView,
                   TagRemoveImage)

urlpatterns = [
    path('api/', TagListAPIView.as_view(), name='tag_list'),
    path('api/<slug>/', TagDetailAPIView.as_view(), name='tag_detail'),
    path('api/<slug>/edit/', TagUpdateAPIView.as_view(), name='tag_update'),
    path('api/<slug>/remove-image/', TagRemoveImage.as_view(), name='tag_remove_image'),
    path('api/<slug>/destroy/', TagDestroyAPIView.as_view(), name='tag_destroy'),
    path('api/create/', TagCreateAPIView.as_view(), name='tag_create'),
]
