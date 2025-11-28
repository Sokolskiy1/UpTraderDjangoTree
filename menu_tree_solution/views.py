from django.shortcuts import render, get_object_or_404

from menu_tree_solution.models import Menu
import sqlite3

# Create your views here.
def menu_tree_view(request,name_item_tree=None):
   print(name_item_tree)
   if (name_item_tree):
      menu = Menu.objects.prefetch_related('parent').filter(name=name_item_tree)

   else:
      menu = Menu.objects.prefetch_related('parent').filter(parent=None)

   print(menu)
   for item in menu.values():
      print(item)
   return render(request, 'menu_tree/menu_tree_main.html',context={'menu':menu})