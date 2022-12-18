from django import forms

class TakeRoom(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()