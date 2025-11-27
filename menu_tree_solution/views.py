from django.shortcuts import render


# Create your views here.
def menu_tree_view(request):
   return render(request, 'menu_tree/menu_tree_main.html')