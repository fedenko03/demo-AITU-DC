from django import forms


class ChooseRoom(forms.Form):
    room = forms.CharField(max_length=25,
                           disabled=False,
                           required=True)


class ChooserData(forms.Form):
    choices = (
        ('Professor', 'Professor'),
        ('Student', 'Student'),
        ('Other', 'Other'),
    )
    fullname = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'id': 'fullname_step4',
                                                             'placeholder': 'ФИО'
                                                             }))
    status = forms.ChoiceField(choices=choices,
                               widget=forms.RadioSelect(),
                               required=True)
