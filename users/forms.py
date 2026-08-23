from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm 
from .models import Profile
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        label="Вкажіть Email", 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Email'})
        )
    username = forms.CharField(
        label="Вкажіть ім'я", 
        required=True, 
        help_text='Не використовуйте символи: @, /, _',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Ім'я"})
        )
    password1 = forms.CharField(
        label="Вкажіть пароль", 
        required=True, help_text='Пароль має містити щонайменше 8 символів',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder':'Пароль'})
            )
    password2 = forms.CharField(
        label="Підтвердіть пароль", 
        required=True, 
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Пароль'})
        )
    # users = forms.ModelChoiceField(queryset=User.objects.all())

    class Meta:
        model = User
        fields = ['username', 'email','password1', 'password2']
        # fields = UserCreationForm.Meta.fields + ('email',)


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(
            label="Вкажіть Email", 
            required=True,
            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Email'})
            )
    username = forms.CharField(
            label="Вкажіть ім'я", 
            required=True, 
            help_text='Не використовуйте символи: @, /, _',
            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Ім'я"})
            )
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileImageForm(forms.ModelForm):
    img = forms.ImageField(
        label='Завантажити фото',
        required=False,
        widget=forms.FileInput()
        )

    gender = forms.ChoiceField(
        label='Стать',
        choices=[
            ('male', 'Чоловіча'),
            ('female', 'Жіноча'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
        )

    email_notifications = forms.BooleanField(
        label='Я погоджуюсь отримувати поштові повідомлення',
        required=False
    )


    class Meta:
        model = Profile
        fields = ['img', 'gender', 'email_notifications']