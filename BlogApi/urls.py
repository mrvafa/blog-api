from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from rest_auth.registration.views import VerifyEmailView

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('rest-auth/', include('rest_auth.urls')),
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
