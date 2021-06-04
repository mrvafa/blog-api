from django.urls import path

from .view import PostListAPIView, PostDetailAPIView, PostUpdateAPIView, PostDestroyAPIView, PostCreateAPIView

urlpatterns = [
    path('api/', PostListAPIView.as_view(), name='post_list'),
    path('api/s/<slug>/', PostDetailAPIView.as_view(), name='post_detail'),
    path('api/s/<slug>/edit/', PostUpdateAPIView.as_view(), name='post_update'),
    path('api/s/<slug>/destroy/', PostDestroyAPIView.as_view(), name='post_destroy'),
    path('api/create/', PostCreateAPIView.as_view(), name='post_create'),
]
