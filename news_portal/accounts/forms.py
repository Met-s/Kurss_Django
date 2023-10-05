from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.core.mail import EmailMultiAlternatives


class CustomSignUpForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        users = Group.objects.get(name="users")
        user.groups.add(users)
        subject = 'Добро пожаловать на наш новостной портал!'
        text = f'{user.username}, вы успешно зарегистрировались!'
        html = (
            f'<b>{user.username}</b>, вы успешно зарегистрировались на '
            f'нашем новостном портале! Добро пожаловать:'
            f'<a href="http://127.0.0.1:8000/news">На сайт</a>!'
        )
        msg = EmailMultiAlternatives(
            subject=subject, body=text, from_email=None, to=[user.email]
        )
        msg.attach_alternative(html, "text/html")
        msg.send()
        return user



# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
#
#
# class SignUpForm(UserCreationForm):
#     email = forms.EmailField(label="Email")
#
#     class Meta:
#         model = User
#         fields = (
#             "username",
#             "email",
#             "password1",
#             "password2",
#         )
