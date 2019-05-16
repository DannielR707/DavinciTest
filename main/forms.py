from django import forms

from main.models import ClientsInfo, Temp


class DocumentForm(forms.ModelForm):
    class Meta:
        model = ClientsInfo
        fields = ('name', 'lastName', 'phoneNumber', 'address', 'campaign')

