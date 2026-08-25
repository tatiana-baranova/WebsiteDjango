from django import forms
from .models import Course


class CourseAddForm(forms.ModelForm):
    slug = forms.SlugField(
        label='Унікальна назва курсу',
        required=True,
        # help_text='Введіть унікальну назву для URL курсу, така назва вже існує',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'URL курсу'
            }
        )
    )
    title = forms.CharField(
        label='Назва курсу',
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Назва курсу'
            }
        )
    )
    description = forms.CharField(
        label='Опис курсу',
        required=True,
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Опис курсу',
                'rows': 5
            }
        )
    )
    image = forms.ImageField(
        label='Зображення курсу',
        required=False,
        widget=forms.ClearableFileInput(
        )
    )

    def clean_slug(self):
        slug = self.cleaned_data['slug']

        if Course.objects.filter(slug=slug).exists():
            raise forms.ValidationError(
                'Курс з такою URL-назвою вже існує.'
            )

        return slug

    class Meta:
        model = Course
        fields = ['slug', 'title', 'description', 'image']