import os
from wsgiref.util import FileWrapper

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views.generic import View
from django.views.generic.edit import CreateView

from .forms import CustomUserCreationForm
from .forms import FileForm
from .helpers import parse_files


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class FileUploadView(View):
    form_class = FileForm
    template_name = 'home.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        request.session['zip_path'] = parse_files(form, request.user.username)
        return redirect('download')


def download_page(request: HttpRequest) -> HttpResponse:
    """Render download page."""
    path = request.session.get('zip_path')
    if not path:
        context = {
            'error': 'Could not extract data. Please ensure that the image contains the text.'}
    else:
        context = {'success': 'Data extracted successfully',
                   'file_name': os.path.basename(request.session['zip_path'])}
    return TemplateResponse(request, 'download.html', context)


def download_text_file(request: HttpRequest) -> HttpResponse:
    """
    Downloads the extracted csv file.
    :param request: HttpRequest
    :return HttpResponse
    """
    path = request.session['zip_path']
    try:
        content = FileWrapper(open(path, 'rb'))
        response = HttpResponse(content, content_type='application/zip')
        response['Content-Length'] = os.path.getsize(path)
        response['Content-Disposition'] = f'attachment; filename={os.path.basename(path)}'
        if response.status_code == 200:
            return response
    except Exception as e:
        print('Extraction is failed due to following exception: \n{}'.format(e))
        messages.error(request, 'Failed to download file, please try again.')
        return redirect('home')
