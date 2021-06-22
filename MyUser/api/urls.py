from django.urls import path

from .view import (
    PrivateUserListAPIView, PrivateUserDetailAPIView, PrivateUserDestroyAPIView, UserEditOwnAPIView,
    UserDestroyOwnAPIView, UserAuthor, MakeUserAdmin, UserChangePasswordAPIView, SetPhoneNumberAPIView,
    SendSMSVerifyCode, PublicUserDetailAPIView, PublicAuthorListAPIView
)

urlpatterns = [
    path('api/private/', PrivateUserListAPIView.as_view(), name='private_user_list'),
    path('api/private/<int:pk>/', PrivateUserDetailAPIView.as_view(), name='private_user_detail'),
    path('api/private/<int:pk>/destroy/', PrivateUserDestroyAPIView.as_view(), name='user_destroy'),

    path('api/authors/', PublicAuthorListAPIView.as_view(), name='public_author_list'),
    path('api/u/<str:username>/', PublicUserDetailAPIView.as_view(), name='public_user_detail'),

    path('api/edit-account/', UserEditOwnAPIView.as_view(), name='edit_account'),
    path('api/delete-account/', UserDestroyOwnAPIView.as_view(), name='delete_account'),
    path('api/change-password/', UserChangePasswordAPIView.as_view(), name='change_password'),
    path('api/send-sms/', SendSMSVerifyCode.as_view(), name='send_sms'),
    path('api/set-phone-number/', SetPhoneNumberAPIView.as_view(), name='set_phone_number_user'),

    path('api/<int:pk>/change-user-author/', UserAuthor.as_view(), name='change_user_author'),
    path('api/<int:pk>/change-user-permissions/', MakeUserAdmin.as_view(), name='change_user_permissions'),
]
