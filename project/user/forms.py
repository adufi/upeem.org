from django import forms


class PortalForm (forms.Form):
    email = forms.EmailField()


class LoginForm (forms.Form):
    email = forms.EmailField()
    password = forms.CharField(min_length=8)
