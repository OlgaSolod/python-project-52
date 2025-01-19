from django import forms
from task_manager.task.models import Task
from django.contrib.auth import get_user_model
from task_manager.status.models import Status
from task_manager.label.models import Label
import django_filters

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
    labels = forms.ModelMultipleChoiceField(
        queryset=Label.objects.all(),
        required=False,
        label="Метки",
        widget=forms.SelectMultiple(attrs={"class": "form-select"} ),
    )


    class Meta:
        model = Task    
        fields = ["name", 'description', 'status', 'executor', 'labels']
        labels = {"name": "Имя"}


class UpdateTaskForm(CreateTaskForm):
    labels = forms.ModelMultipleChoiceField(
        queryset=Label.objects.all(),
        required=False,
        label="Метки",
        widget=forms.SelectMultiple(attrs={"class": "form-select"}),
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            # Устанавливаем начальные значения для поля labels
            self.fields['labels'].initial = self.instance.labels.all()
