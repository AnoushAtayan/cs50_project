from django.contrib.auth.decorators import login_required
from django.urls import path, re_path

from .views import SignUpView, FileUploadView, download_page, download_text_file

urlpatterns = [
    path('', login_required(
        FileUploadView.as_view(), login_url='users/login/'), name='home'),
    path('download/', download_page, name='download'),
    re_path('^download/.*zip/$', download_text_file, name='download_zip'),
    path('signup/', SignUpView.as_view(), name='signup'),
]
