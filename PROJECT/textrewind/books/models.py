from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    additions = models.ManyToManyField(
        User, related_name="addition", blank=True, default=None)
    gendre = models.CharField("Жандр", max_length=20)
    title = models.CharField("Название", max_length=20)
    author = models.CharField("Автор", max_length=20)
    text = models.CharField("Текст книги", max_length=2000000,  default='')
    book_image = models.ImageField("Изображение", upload_to="bookimage/",  default='')
    public_active =  models.BooleanField("Проверенная книга", default=False)
    public = models.BooleanField("Публичная книга", default=False)

    def __str__(self):
        return self.title


    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

class Percent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    percent = models.IntegerField("Процент прочитаного", default=0)
    def __str__(self):
        return str(self.percent)

    class Meta:
        verbose_name = "Процент прочитаного"
        verbose_name_plural = "Проценты прочитаного"