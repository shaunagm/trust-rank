from django import forms

from django.contrib.auth.models import User

class SignUpForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True

    def save(self, commit=True):
        instance = super(SignUpForm, self).save(commit=False)
        instance.is_active = False # Users should not be able to log in until email is confirmed
        instance.set_password(self.cleaned_data["password"])
        instance.save()
        return instance
