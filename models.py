from django.db import models

class Settings(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название сайта")
    description = models.TextField(verbose_name="Описание сайта")
    logo = models.ImageField(upload_to="settings/logos/", verbose_name="Логотип сайта")
    icon = models.ImageField(upload_to="settings/icons/", verbose_name="Иконка сайта")
    email = models.EmailField(verbose_name="Контактный email")
    phone = models.CharField(max_length=20, verbose_name="Номер телефона")
    locate = models.CharField(max_length=255, verbose_name="Адрес (локация)")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Настройка"
        verbose_name_plural = "Настройки"