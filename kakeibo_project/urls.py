from django.contrib import admin
from django.urls import path, include
from kakeibo_app import views as kakeibo_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', kakeibo_views.login_view, name='login'),
    path('logout/', kakeibo_views.logout_view, name='logout'),
    path('kakeibo/', include('kakeibo_app.urls', namespace='kakeibo_app')),
] 