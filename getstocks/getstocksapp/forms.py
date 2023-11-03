from django import forms
from .models import Market

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField()
    name_for_ticker_in_file = forms.CharField(required=False, max_length=100)
    market = forms.ModelChoiceField(queryset=Market.objects.all())