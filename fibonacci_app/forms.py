from django import forms


class CreateNewCalculation(forms.Form):
    number = forms.IntegerField(
        label="Number",
        min_value=0,
        max_value=50,
        widget=forms.TextInput(attrs={"class": "input"}),
    )
