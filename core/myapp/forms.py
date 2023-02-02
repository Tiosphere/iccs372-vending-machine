from django import forms
from myapp.models import Machine, Snack

""" Form module for myapp application"""


class SnackForm(forms.ModelForm):
    """Form for create and edit Snack model."""

    class Meta:  # noqa: ignore=D106
        model = Snack
        fields = ["name"]


class MachineForm(forms.ModelForm):
    """Form for create and edit Machine model."""

    class Meta:  # noqa: ignore=D106
        model = Machine
        fields = ["name", "location"]
