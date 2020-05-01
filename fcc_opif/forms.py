from django import forms

class FileFormForm(forms.Form):
    url = forms.CharField()
    name = forms.CharField()
    boxes = forms.CharField(widget=forms.HiddenInput())