from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View
from django.views.generic.edit import CreateView

from .forms import CustomUserCreationForm
from .forms import FileForm
from .helpers import get_file_paths


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class FileUploadView(View):
    form_class = FileForm
    success_url = reverse_lazy('home')
    template_name = 'home.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        img_paths, txt_paths = get_file_paths(form)
        # fixme handle
        return redirect(self.success_url)
