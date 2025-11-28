from urllib.parse import urlparse
from django import template
from django.db import connection
from menu_tree_solution.models import Menu

register = template.Library()


@register.inclusion_tag('menu_tree/menu_tree_main.html', takes_context=True)
def draw_menu(context, menu_item,current_menu=None):
    return context