from django import forms

class UrlForm(forms.Form):
    url = forms.URLField(label="", max_length=200, required=True, widget=forms.TextInput(attrs={"placeholder": "Example.com", "class": "form-control"}))