from django.urls import path

from .view import (TagListAPIView, TagDetailAPIView, TagUpdateAPIView, TagDestroyAPIView, TagCreateAPIView,)

urlpatterns = [
    path('api/', TagListAPIView.as_view(), name='tag_list'),
    path('api/s/<slug>/', TagDetailAPIView.as_view(), name='tag_detail'),
    path('api/s/<slug>/edit/', TagUpdateAPIView.as_view(), name='tag_update'),
    path('api/s/<slug>/destroy/', TagDestroyAPIView.as_view(), name='tag_destroy'),
    path('api/create/', TagCreateAPIView.as_view(), name='tag_create'),
]
