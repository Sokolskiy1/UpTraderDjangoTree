from django.shortcuts import render

# Create your views here.
def menu_tree_view(request, name_item_tree=None):
    return render(request, 'menu_tree/main.html')