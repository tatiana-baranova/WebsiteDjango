from django.db import models
from django.urls import reverse

class Course(models.Model):
    slug = models.SlugField('Унікальна назва курсу')
    title = models.CharField('Назва курса', max_length=120)
    description = models.TextField('Опис курсу')
    image = models.ImageField('Зображення', default='default.png', upload_to='courses_images')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('course-detail', kwargs={'slug': self.slug})

    # class Meta:
