from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class CustomSignUpForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        users = Group.objects.get(name="users")
        user.groups.add(users)
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
