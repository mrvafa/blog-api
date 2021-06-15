from django.urls import path

from .view import (UserListAPIView, UserDetailAPIView, UserDestroyAPIView, UserEditOwnAPIView, UserDestroyOwnAPIView,
                   UserAuthor, MakeUserAdmin, UserChangePasswordAPIView, SetPhoneNumberAPIView)

urlpatterns = [
    path('api/', UserListAPIView.as_view(), name='user_list'),
    path('api/<int:pk>/', UserDetailAPIView.as_view(), name='user_detail'),
    path('api/<int:pk>/destroy/', UserDestroyAPIView.as_view(), name='user_destroy'),

    path('api/edit-account/', UserEditOwnAPIView.as_view(), name='edit_account'),
    path('api/delete-account/', UserDestroyOwnAPIView.as_view(), name='delete_account'),
    path('api/change-password/', UserChangePasswordAPIView.as_view(), name='change_password'),
    path('api/set-phone-number/', SetPhoneNumberAPIView.as_view(), name='set_phone_number_user'),

    path('api/<int:pk>/change-user-author/', UserAuthor.as_view(), name='change_user_author'),
    path('api/<int:pk>/change-user-permissions/', MakeUserAdmin.as_view(), name='change_user_permissions'),
]
