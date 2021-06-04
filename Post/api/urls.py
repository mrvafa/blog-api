from django.urls import path

from .view import PostListAPIView, PostDetailAPIView, PostUpdateAPIView, PostDestroyAPIView, PostCreateAPIView

urlpatterns = [
    path('api/', PostListAPIView.as_view(), name='post_list'),
    path('api/<slug>/', PostDetailAPIView.as_view(), name='post_detail'),
    path('api/<slug>/edit/', PostUpdateAPIView.as_view(), name='post_update'),
    path('api/<slug>/destroy/', PostDestroyAPIView.as_view(), name='post_destroy'),
    path('api/create/', PostCreateAPIView.as_view(), name='post_create'),
]
