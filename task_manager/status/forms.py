from django import forms
from task_manager.status.models import Status

class CreateStatusForm(forms.ModelForm):
    #name = forms.CharField(max_length=100, label="Имя", blank=False)
    class Meta:
        model = Status
        fields = ['name']
        labels = {
            "name": "Имя"
        }

class UpdateStatusForm(CreateStatusForm):
    pass
