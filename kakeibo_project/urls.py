from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('kakeibo/', include('kakeibo_app.urls', namespace='kakeibo_app')),
] 