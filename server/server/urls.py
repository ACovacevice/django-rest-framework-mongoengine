from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url
from django.contrib import admin

from users.views import *

from server.views import *
from server.routers import HybridRouter

# We use a single global DRF Router that routes views from all apps in project
router = HybridRouter()

# app views and viewsets
router.add_api_view(r'auth', url(r'^auth/$', ObtainAuthToken.as_view(), name=r"auth"))
router.add_api_view(r'register', url(r'^register/$', Register.as_view(), name=r"register"))
router.register(r'users', UserViewSet, r'users')

urlpatterns = [

    # root view of our REST api, generated by Django REST Framework's router
    url(r'^api/', include(router.urls, namespace='api')),

    # index page should be served by django to set cookies, headers etc.
    url(r'^$', index_view, {}, name='index'),
    
]

# let django built-in server serve static and media content
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
