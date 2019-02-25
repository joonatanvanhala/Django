from django.conf.urls import url
from . import views
from django.urls import path, include
from rest_framework import serializers, viewsets, routers, mixins
from .api import emissionsAPIview
from django.db import models
from django.conf import settings
from django.http import JsonResponse


urlpatterns = [
    path('', views.index, name='index'),
    path('country', views.search, name='search')
];


router = routers.DefaultRouter()
router.register('api/emissions', emissionsAPIview, base_name='emissions_api')
urlpatterns += router.urls
