from django import forms
from .models import CsvFile

class CsvFileForm(forms.ModelForm):
    class Meta:
        model = CsvFile
        fields = ["name", "description", "file"]
