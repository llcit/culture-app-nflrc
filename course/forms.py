from django import forms
from django.contrib.auth.models import User


class SignUpForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].required = False
        self.fields['password'].required = False
        self.fields['email'].required = True

    class Meta:
        model = User
        fields = ('email','username', 'password')
        widgets = {
            'username': forms.HiddenInput(),
            'password': forms.HiddenInput()

        }