from importlib.resources import path
import os

from django.conf import settings
from django.core.files.storage import default_storage, FileSystemStorage
from django.core.management.base import BaseCommand
from django.core.management import call_command

from menus.models import Menu, MenuItem, SubmenuItem
from home.models import HomePage

from wagtail.core.models import Site, Page


class Command(BaseCommand):

    help = 'It seeds the database'


    #def _create_pages(self):
    #    news1 = NewsDetailPage(title='An Article', slug='article-1',
     #                           depth=3, path='000100010001')
        
     #   root_page.add_child(instance=new_home)                        
     #   news1.save()



    def _create_menus(self):
        if not Menu.objects.filter(slug='navbar').exists():
            navbar = Menu(title='Navbar', slug='navbar')
            navbar.save()
        if not Menu.objects.filter(slug='footer').exists():
            footer = Menu(title='Footer', slug='footer')
            footer.save()

        navbar = Menu.objects.get(slug='navbar')
        navbar.menu_items.add(MenuItem(link_title='Home', link_url='/'))
        navbar.menu_items.add(MenuItem(link_title='News & Events', link_url='/'))
            
        navbar.menu_items.add(MenuItem(link_title='Partners', link_url='/'))
        navbar.menu_items.add(MenuItem(link_title='Results', link_url='/'))
        navbar.menu_items.add(MenuItem(link_title='Synergies', link_url='/'))
        navbar.menu_items.add(MenuItem(link_title='Contact', link_url='/'))
        navbar.save()
        
        newsevent = MenuItem.objects.get(link_title='News & Events')
        newsevent.submenu_items.add(SubmenuItem(link_title='News', link_url='/'))
        newsevent.submenu_items.add(SubmenuItem(link_title='Events', link_url='/'))
        newsevent.submenu_items.add(SubmenuItem(link_title='Publications', link_url='/'))
        newsevent.save()

        partners = MenuItem.objects.get(link_title='Partners')
        partners.submenu_items.add(SubmenuItem(link_title='Partner 1', link_url='/'))
        partners.submenu_items.add(SubmenuItem(link_title='Partner 2', link_url='/'))
        partners.submenu_items.add(SubmenuItem(link_title='Partner 3', link_url='/'))
        partners.save()

        results = MenuItem.objects.get(link_title='Results')
        results.submenu_items.add(SubmenuItem(link_title='Result 1', link_url='/'))
        results.submenu_items.add(SubmenuItem(link_title='Result 2', link_url='/'))
        results.submenu_items.add(SubmenuItem(link_title='Result 3', link_url='/'))
        results.save()

        return
        

    def _delete_wagtail(self):

        if Page.objects.filter(slug='home').exists():
            root_page = Page.objects.get(slug="home").get_parent().specific
            new_home = HomePage(title='Home', slug='new_home',
                                depth=2, path='00010001')
            root_page.add_child(instance=new_home)
            new_home.save()

            site = Site.objects.update(
                root_page=new_home, hostname='localhost')

            home = Page.objects.get(slug='home')
            home.delete()
            home = HomePage.objects.get(slug='new_home')
            home.slug = 'home'
            home.save()

            return
           

    def handle(self, *args, **options):
        self._delete_wagtail()
        self._create_menus()

    print("Seeded database")
