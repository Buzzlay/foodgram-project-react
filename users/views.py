from django.views.generic import CreateView
from django.urls import reverse_lazy

from .forms import CreationForm


class Registration(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/registration.html'
