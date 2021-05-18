from django.urls import path

from .view import TagListAPIView, TagDetailAPIView, TagUpdateAPIView, TagDestroyAPIView, TagCreateAPIView

urlpatterns = [
    path('api/', TagListAPIView.as_view(), name='tag_list'),
    path('api/<int:pk>/', TagDetailAPIView.as_view(), name='tag_detail'),
    path('api/<int:pk>/edit/', TagUpdateAPIView.as_view(), name='tag_update'),
    path('api/<int:pk>/destroy/', TagDestroyAPIView.as_view(), name='tag_destroy'),
    path('api/create/', TagCreateAPIView.as_view(), name='tag_create'),
]
