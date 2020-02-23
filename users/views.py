from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View
from django.views.generic.edit import CreateView

from .forms import CustomUserCreationForm
from .forms import FileForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class FileUploadView(View):
    form_class = FileForm
    success_url = reverse_lazy('home')
    template_name = 'file_upload.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            return redirect(self.success_url)
        else:
            return render(request, self.template_name, {'form': form})
