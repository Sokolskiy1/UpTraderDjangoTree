from django.shortcuts import render

from menu_tree_solution.models import Menu


# Create your views here.
def menu_tree_view(request):
   menu = Menu.objects.prefetch_related('parent').filter(parent=None)
   print(menu.first().children.all())
   return render(request, 'menu_tree/menu_tree_main.html',context={'menu':menu})