from django import forms 
from .models import Market
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField()
    name_for_ticker_in_file = forms.CharField(required=False, max_length=100)
    market = forms.ModelChoiceField(queryset=Market.objects.all())


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label='Email')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'custom-form-field'
        self.fields['username'].label = 'Login'
        self.fields['username'].help_text = ''

        self.fields['email'].widget.attrs['class'] = 'custom-form-field'

        self.fields['password1'].widget.attrs['class'] = 'custom-form-field'
        self.fields['password1'].label = 'Password'
        self.fields['password1'].help_text = ''

        self.fields['password2'].widget.attrs['class'] = 'custom-form-field'
        self.fields['password2'].label = 'Confirm Password'
        self.fields['password2'].help_text = ''


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'custom-form-field'
        self.fields['password'].widget.attrs['class'] = 'custom-form-field'
