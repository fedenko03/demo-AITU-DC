from django import forms


class ChooseRoom(forms.Form):
    room = forms.CharField(max_length=25, disabled=False)


class ChooserData(forms.Form):
    fullname = forms.CharField(max_length=50)
    status = forms.CharField(
        choices=[(1, 'Professor'), (2, 'Student'), (3, 'Other')]
    )
