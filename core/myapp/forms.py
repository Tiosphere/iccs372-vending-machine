from django import forms
from myapp.models import Snack, Stock, Machine


class SnackForm(forms.ModelForm):
    class Meta:
        model = Snack
        fields = ["name"]


class StockForm(forms.ModelForm):
    """
    Require all fields in Stock model
    """

    class Meta:
        model = Stock
        fields = "__all__"


class MachineForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = ["location"]
