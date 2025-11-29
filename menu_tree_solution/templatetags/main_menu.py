from django import template
from django.db import connection
from menu_tree_solution.models import Menu

register = template.Library()


def get_menu_path(name_item_tree):
    with connection.cursor() as cursor:
        cursor.execute("""
                   WITH RECURSIVE menu_path AS (
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
                           mp.level - 1,
                           'parent' as direction
                       FROM menu_tree_solution_menu m
                       INNER JOIN menu_path mp ON m.id = mp.parent_id
                       WHERE mp.direction IN ('current', 'parent')

                       UNION ALL

                       SELECT
                           m.id,
                           m.name,
                           m.url,
                           m.parent_id,
                           mp.level + 1,
                           'child' as direction
                       FROM menu_tree_solution_menu m
                       INNER JOIN menu_path mp ON m.parent_id = mp.id
                       WHERE mp.direction = 'current'
                   )
                   SELECT DISTINCT * FROM menu_path
                   ORDER BY
                       level ASC;
               """, [name_item_tree])

        return cursor.fetchall()


@register.inclusion_tag('menu_tree/menu_tree_main.html', takes_context=True)
def draw_menu(context, menu_item, current_menu=None):
    request = context.get('request')
    if not request:
        return {
            'parents': None,
            'current': [],
            'childrens': None
        }

    path_parts = request.path.strip('/').split('/')
    name_item_tree = None
    if len(path_parts) >= 2 and path_parts[-2] == 'menu_tree':
        name_item_tree = path_parts[-1] if path_parts[-1] else None

    if name_item_tree:
        result = get_menu_path(name_item_tree)

        menu_chain = []
        for row in result:
            menu_chain.append({
               'id': row[0],
               'name': row[1],
               'url': row[2],
               'parent_id': row[3],
               'level': row[4]
            })

        parents = [obj for obj in menu_chain if obj.get('level', 0) < 0]
        current = [obj for obj in menu_chain if obj.get('level', 0) == 0]
        childrens = [obj for obj in menu_chain if obj.get('level', 0) > 0]

        return {
           'parents': parents,
           'current': current,
           'childrens': childrens
        }

    else:
        menus = Menu.objects.filter(parent=None).prefetch_related('children')
        return {
           'parents': None,
           'current': menus,
           'childrens': None
        }