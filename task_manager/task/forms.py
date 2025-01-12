from django import forms
from task_manager.task.models import Task
from django.contrib.auth import get_user_model
from task_manager.status.models import Status

User = get_user_model()


class CreateTaskForm(forms.ModelForm):

    description = forms.CharField(required=False, widget=forms.Textarea, label='Описание')
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        label="Статус",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    executor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Исполнитель",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Task
        fields = ["name", 'description', 'status', 'executor']
        labels = {"name": "Имя"}


class UpdateTaskForm(CreateTaskForm):
    pass