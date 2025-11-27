from django.contrib import admin

from .models import Menu
from django.db import models

# Register your models here.

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['name','parent']

