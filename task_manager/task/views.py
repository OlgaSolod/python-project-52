from django.shortcuts import render
from django.views.generic.list import ListView
from django_filters.views import FilterView
from task_manager.task.models import Task
from task_manager.task.filters import TaskFilter
from django.contrib.auth import get_user_model
from task_manager.task.forms import CreateTaskForm, UpdateTaskForm
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

User = get_user_model()
class TasksListView(LoginRequiredMixin, FilterView):
    model = Task
    template_name = "task/tasks.html"
    context_object_name = "tasks"
    login_url = "/login"
    redirect_field_name = ""
    filterset_class=TaskFilter

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        messages.error(self.request, "Вы не авторизованы! Пожалуйста, выполните вход.")
        return super().handle_no_permission()


class CreateTaskView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = "task/create.html"
    login_url = "/login"
    redirect_field_name = ""
    form_class = CreateTaskForm
    success_url = reverse_lazy("tasks_list")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        messages.error(self.request, "Вы не авторизованы! Пожалуйста, выполните вход.")
        return super().handle_no_permission()

    def form_valid(self, form):
        form.instance.creator_id = self.request.user.id
        self.object = form.save()  # Сохраняем объект
        messages.success(self.request, "Задача успешно создана")
        return super().form_valid(form)


class UpdateTaskView(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = "task/update.html"
    login_url = "/login"
    redirect_field_name = ""
    form_class = UpdateTaskForm
    success_url = reverse_lazy("tasks_list")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        obj = self.get_object()
        if request.user.id != obj.creator_id:
            messages.error(
                request, "Вы не можете изменять данные других пользователей."
            )
            return redirect("tasks_list")
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        messages.error(self.request, "Вы не авторизованы! Пожалуйста, выполните вход.")
        return super().handle_no_permission()

    def form_valid(self, form):
        Task = form.save(commit=False)
        if form.cleaned_data.get("name"):
            Task.save()
            form.save_m2m()
            messages.success(self.request, "Задача успешно изменена")
        return super().form_valid(form)


class DeleteTaskView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "task/delete.html"
    login_url = "/login"
    redirect_field_name = ""
    success_url = reverse_lazy("tasks_list")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
       
        obj = self.get_object()
        if request.user.id != obj.creator_id:
            messages.error(
                request, "Вы не можете изменять данные других пользователей."
            )
            return redirect("tasks_list")
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        messages.error(self.request, "Вы не авторизованы! Пожалуйста, выполните вход.")
        return super().handle_no_permission()

    def form_valid(self, form):
        messages.success(self.request, "Задача успешно удалена")
        return super().form_valid(form)
