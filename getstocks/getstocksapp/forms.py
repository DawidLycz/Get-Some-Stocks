from django import forms 
from .models import Market, Wallet, WalletRecord
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField()
    name_for_ticker_in_file = forms.CharField(required=False, max_length=100)
    market = forms.ModelChoiceField(queryset=Market.objects.all())


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label='Email', required=False)

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

class UserProfileEditForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['class'] = 'custom-form-field'
        self.fields['last_name'].widget.attrs['class'] = 'custom-form-field'
        self.fields['email'].widget.attrs['class'] = 'custom-form-field'


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'custom-form-field'
        self.fields['password'].widget.attrs['class'] = 'custom-form-field'


class WalletEditForm(forms.ModelForm):
    name = forms.CharField

    class Meta:
        model = Wallet
        fields = ['name']

    def __init__(self, *args, user=None, ticker_id=None, **kwargs):
        super(WalletEditForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'custom-form-field'


class WalletInviteForm(forms.ModelForm):
    guests = forms.ModelChoiceField(queryset=User.objects.none(), label='Guest')

    class Meta:
        model = Wallet
        fields = ['guests']

    def __init__(self, *args, user=None, ticker_id=None, **kwargs):
        super(WalletInviteForm, self).__init__(*args, **kwargs)
        self.fields['guests'].queryset = User.objects.exclude(pk=user.pk)
        self.fields['guests'].widget.attrs['class'] = 'custom-form-field'


class WalletRecordForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=1)

    class Meta:
        model = WalletRecord
        fields = ['quantity', 'wallet']

    def __init__(self, *args, user=None, ticker_id=None, **kwargs):
        super(WalletRecordForm, self).__init__(*args, **kwargs)
        self.fields['wallet'].queryset = Wallet.objects.filter(owner=user)
        self.fields['wallet'].empty_label = None
        self.fields['quantity'].widget.attrs['class'] = 'custom-form-field'
        self.fields['wallet'].widget.attrs['class'] = 'custom-form-field'


class RecordChangeWalletForm(forms.ModelForm):
    class Meta:
        model = WalletRecord
        fields = ['wallet']

    def __init__(self, *args, user=None, ticker_id=None, **kwargs):
        super(RecordChangeWalletForm, self).__init__(*args, **kwargs)
        self.fields['wallet'].queryset = Wallet.objects.filter(owner=user)
        self.fields['wallet'].empty_label = None
        self.fields['wallet'].widget.attrs['class'] = 'custom-form-field'


class RecordEditForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=1)

    class Meta:
        model = WalletRecord
        fields = ['name', 'quantity']

    def __init__(self, *args, user=None, ticker_id=None, **kwargs):
        super(RecordEditForm, self).__init__(*args, **kwargs)
        self.fields['quantity'].widget.attrs['class'] = 'custom-form-field'
        self.fields['name'].widget.attrs['class'] = 'custom-form-field'

