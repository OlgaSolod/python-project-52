from django.shortcuts import redirect
from django.views.generic.list import ListView
from task_manager.user.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView
from django.views.generic.edit import UpdateView, DeletionMixin
from task_manager.user.forms import (
    CustomRegistrationForm,
    CustomUpdateUserForm
)
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from task_manager.task.models import Task

# Create your views here.


class UsersListView(ListView):
    model = User
    template_name = "user/users.html"
    context_object_name = "users"


class RegisterView(CreateView):
    model = User
    form_class = CustomRegistrationForm
    template_name = "user/create.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        messages.success(self.request, "Пользователь успешно зарегистрирован")
        return super().form_valid(form)


class CustomLoginView(LoginView):
    model = User
    form_class = AuthenticationForm
    template_name = "user/login.html"
    next_page = reverse_lazy("main")

    def form_valid(self, form):
        messages.success(self.request, "Вы залогинены")
        return super().form_valid(form)


class CustomLogoutView(SuccessMessageMixin, LogoutView):
    model = User
    next_page = reverse_lazy("main")

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "Вы разлогинены")
        return super().dispatch(request, *args, **kwargs)


class CustomUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = CustomUpdateUserForm
    template_name = "user/update.html"
    success_url = reverse_lazy("users_list")
    login_url = "/login"
    redirect_field_name = ""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        obj = self.get_object()
        if obj != request.user:
            messages.error(request, "У вас нет прав для изменения")
            return redirect("users_list")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        if form.cleaned_data.get("password1"):
            user.set_password(
                form.cleaned_data["password1"]
            )  # Устанавливаем новый пароль
        user.save()  # Сохраняем изменения в базу
        messages.success(self.request, "Пользователь успешно изменен.")
        logout(self.request)  # Разлогиниваем пользователя после изменения
        return super().form_valid(form)

    def handle_no_permission(self):
        messages.error(
            self.request, "Вы не авторизованы! Пожалуйста, выполните вход."
            )
        return super().handle_no_permission()


class CustomDeleteView(LoginRequiredMixin, DeleteView, DeletionMixin):
    model = User
    template_name = "user/delete.html"
    success_url = reverse_lazy("users_list")
    login_url = "/login"
    redirect_field_name = ""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        obj = self.get_object()
        if obj != request.user:
            messages.error(request, "У вас нет прав для изменения")
            return redirect("users_list")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if Task.objects.filter(creator=self.request.user).exists():
            messages.error(
                self.request,
                "Невозможно удалить пользователя, потому что он используется",
            )
            return redirect("users_list")
        messages.success(self.request, "Пользователь успешно удален")
        logout(self.request)
        return super().form_valid(form)

    def handle_no_permission(self):
        messages.error(
            self.request, "Вы не авторизованы! Пожалуйста, выполните вход."
            )
        return super().handle_no_permission()
