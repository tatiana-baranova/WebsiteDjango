from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

class Course(models.Model):
    slug = models.SlugField('Унікальна назва курсу', unique=True)
    title = models.CharField('Назва курса', max_length=120)
    description = models.TextField('Опис курсу')
    image = models.ImageField('Зображення', default='default.png', upload_to='courses_images')
    is_free = models.BooleanField('Безкоштовно?', default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('course-detail', kwargs={'slug': self.slug})


class Lesson(models.Model):
    slug = models.SlugField('Унікальна назва урока')
    title =models.CharField('Назва урока', max_length=120)
    description = models.TextField('Опис урока')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Який курс?')
    number = models.IntegerField('Номер урока')
    video = models.CharField('Відео Url',  max_length=100)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('lesson-detail', kwargs={'slug': self.course.slug, 'lesson_slug': self.slug})

class Comment(models.Model):
    user = models.ForeignKey(User,verbose_name='Автор коментаря', on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson,verbose_name='Урок', on_delete=models.CASCADE)
    message = models.TextField(verbose_name='Коментар')

    def __str__(self):
        return f'{self.user.username} — {self.lesson.title}'