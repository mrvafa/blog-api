from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from rest_auth.registration.views import VerifyEmailView
from rest_auth.views import (PasswordResetView, PasswordResetConfirmView, LoginView, UserDetailsView,
                             PasswordChangeView, )

urlpatterns = [
                  path('admin/', admin.site.urls),
                  re_path(r'^rest-auth/password/reset/$', PasswordResetView.as_view(), name='rest_password_reset'),
                  re_path(r'^rest-auth/password/reset/confirm/$', PasswordResetConfirmView.as_view(),
                          name='rest_password_reset_confirm'),
                  re_path(r'^rest-auth/login/$', LoginView.as_view(), name='rest_login'),
                  re_path(r'^rest-auth/user/$', UserDetailsView.as_view(), name='rest_user_details'),
                  re_path(r'^rest-auth/password/change/$', PasswordChangeView.as_view(),
                          name='rest_password_change'),
                  path('rest-auth/registration/', include('rest_auth.registration.urls')),
                  re_path(r'^account-confirm-email$', VerifyEmailView.as_view(),
                          name='account_email_verification_sent'),
                  re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$', VerifyEmailView.as_view(),
                          name='account_confirm_email'),
                  path('ckeditor/', include('ckeditor_uploader.urls')),

                  path('post/', include('Post.urls')),
                  path('tag/', include('Tag.urls')),
                  path('profile/', include('MyUser.urls')),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
