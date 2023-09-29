from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .forms import CustomSignUpForm
from django.urls import reverse_lazy


class SignUp(CreateView):
    model = User
    form_class = CustomSignUpForm
    success_url = reverse_lazy('news')
    template_name = 'registration/signup.html'
