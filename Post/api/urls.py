from django.urls import path

from .view import PostListAPIView, PostDetailAPIView, PostUpdateAPIView, PostDestroyAPIView, PostCreateAPIView

urlpatterns = [
    path('api/', PostListAPIView.as_view(), name='post_list'),
    path('api/<int:pk>/', PostDetailAPIView.as_view(), name='post_detail'),
    path('api/<int:pk>/edit/', PostUpdateAPIView.as_view(), name='post_update'),
    path('api/<int:pk>/destroy/', PostDestroyAPIView.as_view(), name='post_destroy'),
    path('api/create/', PostCreateAPIView.as_view(), name='post_create'),
]
