from django.conf import settings
from django.conf.urls import url
import django.views.static
from django.urls import path, include, re_path
from rest_auth.registration.views import VerifyEmailView
from rest_auth.views import (PasswordResetView, PasswordResetConfirmView, LoginView, UserDetailsView, )

urlpatterns = [
    re_path(r'^register/', include('rest_auth.registration.urls')),
    re_path(r'^password/reset/$', PasswordResetView.as_view(), name='rest_password_reset'),
    re_path(r'^password/reset/confirm/$', PasswordResetConfirmView.as_view(),
            name='rest_password_reset_confirm'),
    re_path(r'^login/$', LoginView.as_view(), name='rest_login'),
    re_path(r'^profile/$', UserDetailsView.as_view(), name='rest_user_details'),
    re_path(r'^account-confirm-email/$', VerifyEmailView.as_view(),
            name='account_email_verification_sent'),
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$', VerifyEmailView.as_view(),
            name='account_confirm_email'),
    path('ckeditor/', include('ckeditor_uploader.urls')),

    path('post/', include('Post.urls')),
    path('tag/', include('Tag.urls')),
    path('profile/', include('MyUser.urls')),

    url(r'^static/(?P<path>.*)$', django.views.static.serve,
        {'document_root': settings.STATIC_ROOT, 'show_indexes': settings.DEBUG}),
]
