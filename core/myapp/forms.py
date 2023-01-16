from django import forms
from myapp.models import Snack, Machine


class SnackForm(forms.ModelForm):
    class Meta:
        model = Snack
        fields = ["name"]


class MachineForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = ["name", "location"]
