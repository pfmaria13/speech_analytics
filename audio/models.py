from django.db import models


class Recordings(models.Model):
    speed = models.TextField('Скорость')
    text = models.TextField('Текст')

    def __str__(self):
        return self.speed

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'


