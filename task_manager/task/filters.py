import django_filters
from django.contrib.auth import get_user_model
from task_manager.status.models import Status
from task_manager.label.models import Label
from .models import Task
from django import forms

User = get_user_model()


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(), label="Статус",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(), label="Исполнитель",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    label = django_filters.ModelChoiceFilter(
        field_name="labels",
        queryset=Label.objects.all(),
        label="Метка",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    self_tasks = django_filters.BooleanFilter(
        field_name="creator",
        label="Только свои задачи",
        method="filter_self_tasks",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    class Meta:
        model = Task
        fields = ["status", "executor", "label", "self_tasks"]

    def filter_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(creator=self.request.user)
        return queryset
