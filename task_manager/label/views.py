from django.views.generic.list import ListView
from task_manager.label.models import Label
from task_manager.label.forms import CreateLabelForm, UpdateLabelForm
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from task_manager.task.models import Task

# Create your views here.


class LabelsListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = "label/labels.html"
    context_object_name = "labels"
    login_url = "/login"
    redirect_field_name = ""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        messages.error(self.request, "Вы не авторизованы! Пожалуйста, выполните вход.")
        return super().handle_no_permission()


class CreateLabelView(LoginRequiredMixin, CreateView):
    model = Label
    template_name = "label/create.html"
    login_url = "/login"
    redirect_field_name = ""
    form_class = CreateLabelForm
    success_url = reverse_lazy("labels_list")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        messages.error(self.request, "Вы не авторизованы! Пожалуйста, выполните вход.")
        return super().handle_no_permission()

    def form_valid(self, form):
        messages.success(self.request, "Метка успешно создана")
        return super().form_valid(form)


class UpdateLabelView(LoginRequiredMixin, UpdateView):
    model = Label
    template_name = "label/update.html"
    login_url = "/login"
    redirect_field_name = ""
    form_class = UpdateLabelForm
    success_url = reverse_lazy("labels_list")

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
            messages.success(self.request, "Метка успешно изменена")
        return super().form_valid(form)


class DeleteLabelView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = "label/delete.html"
    login_url = "/login"
    redirect_field_name = ""
    success_url = reverse_lazy("labels_list")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        messages.error(self.request, "Вы не авторизованы! Пожалуйста, выполните вход.")
        return super().handle_no_permission()

    def form_valid(self, form):
        label = self.get_object()
        if Task.objects.filter(labels=label).exists():
            messages.error(
                self.request, "Невозможно удалить метку, потому что она используется"
            )
            return redirect("labels_list")
        messages.success(self.request, "Метка успешно удалена")
        return super().form_valid(form)
