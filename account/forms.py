from django import forms

class Deposit(forms.Form):
    amount = forms.DecimalField()