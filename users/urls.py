from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import SignUpView, FileUploadView

urlpatterns = [
    path('', login_required(
        FileUploadView.as_view(template_name='home.html'), login_url='users/login/'), name='home'),
    path('signup/', SignUpView.as_view(), name='signup'),
]
