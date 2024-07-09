"""
URL configuration for bloom project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns 
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from Authorization.views import LoginView, RegistrationView
from Video.views import VideoItemViewSet, video_by_token
from Authorization.utils import activate_user, logout_user
from user.utils import change_profile_img
from user.views import UserViewSet
from Authorization.utils import activate_user,delete_user, logout_user, send_reset_Password_mail_user, reset_password

router = routers.DefaultRouter()

router.register(r"videos", VideoItemViewSet) 
router.register(r"user", UserViewSet, basename="user")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(),name='login'),
    path('register/', RegistrationView.as_view()),
    path("__debug__/", include("debug_toolbar.urls")),
    path('django-rq/', include('django_rq.urls')),
    path('activate/<str:token>/', activate_user, name='activate_user'),
    path('delete_user/<str:token>/', delete_user, name='delete_user'),
    path('logout/<str:token>/', logout_user, name='logout_user'),
    path('resetPasswordMail/', send_reset_Password_mail_user, name='send_reset_Password_mail_user'),
    path('changePicture/<str:token>/', change_profile_img, name='change_profile_img'),
    path('resetPassword/<str:token>/', reset_password, name='reset_password'),
    path('video/<uuid:token>/', video_by_token, name='video_by_token'),
    path('',include(router.urls))
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
