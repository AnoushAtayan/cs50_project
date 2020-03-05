from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('about', login_required(
        TemplateView.as_view(template_name='about.html'), login_url='users/login/'), name='about'),
    path('users/', include('django.contrib.auth.urls')),
]
