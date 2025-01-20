from django import forms
from task_manager.label.models import Label


class CreateLabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ["name"]
        labels = {"name": "Имя"}


class UpdateLabelForm(CreateLabelForm):
    pass
