from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth import authenticate
from .models import Account


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60)
    class Meta:
        model = Account
        fields = ('email', 'password1','password2','first_name','last_name','status','organism','key_words','webpage',
                  'country', 'sex')



class Login_form(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email','password')

    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        if not authenticate(email=email,password=password):
            raise forms.ValidationError('Invalid email or password')


class EditAccountForm(UserChangeForm):

    class Meta:
        model = Account
        fields = ('first_name','last_name','email','webpage','organism','status','key_words')

