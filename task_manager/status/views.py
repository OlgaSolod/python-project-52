from django.views.generic.list import ListView
from task_manager.status.models import Status
from task_manager.status.forms import CreateStatusForm, UpdateStatusForm
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from task_manager.task.models import Task

# Create your views here.


class StatusesListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = "status/statuses.html"
    context_object_name = "statuses"
    login_url = "/login"
    redirect_field_name = ""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        messages.error(self.request, "Вы не авторизованы! Пожалуйста, выполните вход.")
        return super().handle_no_permission()


class CreateStatusView(LoginRequiredMixin, CreateView):
    model = Status
    template_name = "status/create.html"
    login_url = "/login"
    redirect_field_name = ""
    form_class = CreateStatusForm
    success_url = reverse_lazy("statuses_list")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        messages.error(self.request, "Вы не авторизованы! Пожалуйста, выполните вход.")
        return super().handle_no_permission()

    def form_valid(self, form):
        messages.success(self.request, "Статус успешно создан")
        return super().form_valid(form)


class UpdateStatusView(LoginRequiredMixin, UpdateView):
    model = Status
    template_name = "status/update.html"
    login_url = "/login"
    redirect_field_name = ""
    form_class = UpdateStatusForm
    success_url = reverse_lazy("statuses_list")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        messages.error(self.request, "Вы не авторизованы! Пожалуйста, выполните вход.")
        return super().handle_no_permission()

    def form_valid(self, form):
        status = form.save(commit=False)
        if form.cleaned_data.get("name"):
            status.save()
            messages.success(self.request, "Статус успешно изменен.")
        return super().form_valid(form)


class DeleteStatusView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = "status/delete.html"
    login_url = "/login"
    redirect_field_name = ""
    success_url = reverse_lazy("statuses_list")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        messages.error(self.request, "Вы не авторизованы! Пожалуйста, выполните вход.")
        return super().handle_no_permission()

    def form_valid(self, form):
        status = self.get_object()
        if Task.objects.filter(status=status).exists():
            messages.error(
                self.request, "Невозможно удалить статус, потому что он используется"
            )
            return redirect("statuses_list")
        messages.success(self.request, "Статус успешно удален")
        return super().form_valid(form)
