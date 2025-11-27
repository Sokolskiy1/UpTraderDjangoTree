from django.db import models

# Create your models here.


class Menu(models.Model):
    name = models.CharField(max_length=200, unique=True)
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, null=True, blank=True)
    url = models.CharField(max_length=255,default='')


    class Meta:
        verbose_name = ('menu')
        verbose_name_plural = ('menus')

    def __str__(self): return self.name

