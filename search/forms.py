from django import forms

class SearchForm(forms.Form):
    #search = forms.CharField( max_length=100)
    search = forms.CharField(label="", help_text="", widget=forms.TextInput())

class Meta:
    fields=('query')