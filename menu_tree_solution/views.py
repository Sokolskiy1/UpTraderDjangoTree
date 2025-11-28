from django.db import connection
from django.shortcuts import render, get_object_or_404

from menu_tree_solution.models import Menu
import sqlite3

# Create your views here.
def menu_tree_view(request, name_item_tree=None):
   if name_item_tree:
      # Рекурсивный запрос для получения цепочки родителей
      with connection.cursor() as cursor:
         cursor.execute("""
               WITH RECURSIVE menu_path AS (
                   SELECT 
                       id,
                       name,
                       url,
                       parent_id,
                       0 as level
                   FROM menu_tree_solution_menu 
                   WHERE name = %s

                   UNION ALL

                   SELECT 
                       m.id,
                       m.name,
                       m.url,
                       m.parent_id,
                       mp.level + 1
                   FROM menu_tree_solution_menu m
                   INNER JOIN menu_path mp ON m.id = mp.parent_id
               )
               SELECT * FROM menu_path ORDER BY level DESC
           """, [name_item_tree])

         result = cursor.fetchall()

      # Преобразуем результат в удобный формат
      menu_chain = []
      for row in result:
         menu_chain.append({
            'id': row[0],
            'name': row[1],
            'url': row[2],
            'parent_id': row[3],
            'level': row[4]
         })

      # Получаем полные объекты Menu для цепочки
      menu_ids = [item['id'] for item in menu_chain]
      menu_objects = Menu.objects.filter(id__in=menu_ids)

      context = {
         'menu': menu_chain,
         # 'menu_objects': menu_objects
      }

   else:
      # Корневые элементы
      menu = Menu.objects.filter(parent=None)
      context = {'menu': menu}
   print(context)
   return render(request, 'menu_tree/menu_tree_main.html', context)