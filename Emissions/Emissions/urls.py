from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('datahandler.urls')),
    path('admin/', admin.site.urls),
    path('emissions/', include('datahandler.urls'))
]
