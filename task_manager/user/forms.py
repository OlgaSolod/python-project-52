from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError

from task_manager.user.models import User
#from django.contrib.auth.models import User


class CustomAuth(AuthenticationForm):
    pass

class CustomRegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput,
        help_text= """
        <ul>
            <li>Ваш пароль должен содержать как минимум 3 символа.</li>
        </ul>
        """
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput,
        help_text="Для подтверждения введите, пожалуйста, пароль ещё раз."
    )
    class Meta:
        model = User
        fields = ['first_name', 'last_name','username']
        labels = {
            'first_name': "Имя",
            'last_name': 'Фамилия',
            'username': 'Имя пользователя',
        }
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        # Проверяем, что оба поля заполнены
        if password1 and password2:
            if password1 != password2:
                raise ValidationError("Пароли не совпадают.")
        return cleaned_data
                

class CustomUpdateUserForm(CustomRegistrationForm):
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if self.instance.username == username:
            return username
        return super().clean_username()
