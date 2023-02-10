from django import forms

from user.models import Role


class ChooseRoom(forms.Form):
    room = forms.CharField(max_length=25,
                           disabled=False,
                           required=True)


class ChooserData(forms.Form):
    fullname = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'id': 'fullname_step4',
                                                             'placeholder': 'ФИО'
                                                             }))
    role = forms.ChoiceField(choices=[(c.name, c.name) for c in Role.objects.exclude(name='All')],
                             widget=forms.RadioSelect(),
                             required=True)
