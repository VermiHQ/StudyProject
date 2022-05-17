from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth.models import User
from PIL import Image

# надо проработать еще все поля нужные
class Dish(models.Model):
    type = models.ForeignKey('Type', null = True, on_delete = models.PROTECT, verbose_name = 'Категория')
    ingredients = models.ManyToManyField('Ingredient', verbose_name = 'Ингредиенты')
    image = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name = 'Картинка')
    title = models.CharField(max_length = 50, db_index = True, verbose_name = "Блюдо")
    # привязка пользователя
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    recipe = models.TextField(null = True, verbose_name = "Рецепт")
    published = models.DateTimeField(auto_now_add = True, db_index = True, verbose_name = "Опубликовано")
    update_date = models.DateTimeField("Обновлено", auto_now = True)
    likes = models.IntegerField(default=0, verbose_name = "Лайк")
    user_likes = models.TextField(null = True, blank = True, default = '')
    def was_like(self,  user_id):
        user = User(id = user_id)
        if str(user.id) in self.user_likes.split():
            return True
        return False
    # подгоняекм картинку под размеры, не превышающие 580х450
    def save(self):
        super().save()
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 450 or img.width > 580:
                output_size = (450, 580)
                img.thumbnail(output_size)
                img.save(self.image.path)
    # если выложено недавно --> True
    def check_updated(self):
        now = timezone.now()
        return self.published >= now - datetime.timedelta(hours=1)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural = 'Блюд(-а)'
        verbose_name = 'Блюдо'
        ordering = ['-published']

class Type(models.Model):
    name = models.CharField(max_length = 20, db_index = True, verbose_name = 'Тип')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Категории(-й)'
        verbose_name = 'Категория'
        ordering = ['name']

class Ingredient(models.Model):
    name = models.CharField(max_length = 20, null=True, db_index = True, verbose_name = 'Ингредиент')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Ингредиента(-ов/-ы)'
        verbose_name = 'Ингредиент'
        ordering = ['name']

