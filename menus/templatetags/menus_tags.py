from django import template 
from ..models import Menu, SubmenuItem

register = template.Library()

@register.simple_tag()
def get_menu(slug):
	return Menu.objects.get(slug=slug)

@register.simple_tag()
def get_submenu_items():
	return SubmenuItem.objects.all()