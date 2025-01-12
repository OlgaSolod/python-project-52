from django import forms
from task_manager.status.models import Status

class CreateStatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']
        labels = {
            "name": "Имя"
        }

class UpdateStatusForm(CreateStatusForm):
    pass
