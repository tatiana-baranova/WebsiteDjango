from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import os

TYPE_ACCOUNT = (
    ('full', 'Повний пакет'),
    ('free', 'Безкоштовний пакет')
)

class Profile(models.Model):
    user = models.OneToOneField(User,verbose_name='Користувач', on_delete=models.CASCADE)
    img = models.ImageField('Фото користувача', default='default_image.jpg', upload_to='user_images')
    gender = models.CharField(
        verbose_name='Стать',
        max_length=20,
        choices=[
            ('male', 'Чоловіча'),
            ('female', 'Жіноча'),
        ],
        default='male'
    )
    email_notifications = models.BooleanField(
        verbose_name='Отримання повідомлень на пошту',
        default=False
    )
    account_type = models.CharField(
        choices=TYPE_ACCOUNT, default='free', max_length=20
    )

    def __str__(self):
        return f'Профіль користувача {self.user.username}'

    def save(self, *args, **kwargs):
        if self.pk:
            old = Profile.objects.get(pk=self.pk)
            if old.img and old.img != self.img:
                if old.img.name != 'default_image.jpg' and os.path.isfile(old.img.path):
                    os.remove(old.img.path)

        super().save(*args, **kwargs)
        image = Image.open(self.img.path)
        if image.height > 256 or image.width > 256:
            resize = (256, 256)
            image.thumbnail(resize)
            image.save(self.img.path)

    class Meta:
        verbose_name = 'Профіль'
        verbose_name_plural = 'Профіль'


class Payment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Користувач'
    )
    plan = models.CharField(
        'Тариф',
        max_length=50,
        default='full'
    )
    amount = models.DecimalField(
        'Сума',
        max_digits=10,
        decimal_places=2
    )
    order_reference = models.CharField(
        'Номер замовлення',
        max_length=100,
        unique=True
    )
    status = models.CharField(
        'Статус',
        max_length=20,
        default='pending'
    )
    created_at = models.DateTimeField(
        'Дата створення',
        auto_now_add=True
    )

    def __str__(self):
        return f'{self.user.username} — {self.amount} грн'