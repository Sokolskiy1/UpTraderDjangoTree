from urllib.parse import urlparse

from django.db import connection
from django.shortcuts import render

from menu_tree_solution.models import Menu

# Create your views here.
def menu_tree_view(request, name_item_tree=None):
   if name_item_tree:
      with connection.cursor() as cursor:
         cursor.execute("""
                    WITH RECURSIVE menu_path AS (
                        -- Начальная точка: элемент с заданным именем
                        SELECT 
                            id,
                            name,
                            url,
                            parent_id,
                            0 as level,
                            'current' as direction
                        FROM menu_tree_solution_menu 
                        WHERE name = %s
                    
                        UNION ALL
                    
                        SELECT 
                            m.id,
                            m.name,
                            m.url,
                            m.parent_id,
                            mp.level - 1, -- Отрицательные уровни для родителей
                            'parent' as direction
                        FROM menu_tree_solution_menu m
                        INNER JOIN menu_path mp ON m.id = mp.parent_id
                        WHERE mp.direction IN ('current', 'parent') -- Только от текущего и родителей
                    
                        UNION ALL
                    
                        -- Часть 2: Идем вниз к детям (только один уровень)
                        SELECT 
                            m.id,
                            m.name,
                            m.url,
                            m.parent_id,
                            mp.level + 1, -- Положительные уровни для детей
                            'child' as direction
                        FROM menu_tree_solution_menu m
                        INNER JOIN menu_path mp ON m.parent_id = mp.id
                        WHERE mp.direction = 'current' -- Только от исходного элемента
                    )
                    SELECT DISTINCT * FROM menu_path 
                    ORDER BY 
                        level ASC; 
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

      # print(menu_chain,type(menu_chain))
      parents = [obj for obj in menu_chain if obj.get('level', 0) < 0]
      current = [obj for obj in menu_chain if obj.get('level', 0) == 0]
      childrens = [obj for obj in menu_chain if obj.get('level', 0) > 0]
      # print("ptr", parents, current, childrens)
      context = {
         # 'menu': menu_chain,
         # 'menu_objects': menu_objects
         'parents': parents,
         'current': current,
         'childrens': childrens
      }

   else:
      # Корневые элементы
      menus = Menu.objects.filter(parent=None).prefetch_related('children')
      # menus_element = []
      # for menu in menus:
      #    child = menu.children.all()
      #    menus_element.append(child)

      context = {
         'parents': None,
         'current': menus,
         'childrens': None
      }
   print(context)
   return render(request, 'menu_tree/menu_tree_main.html', context)