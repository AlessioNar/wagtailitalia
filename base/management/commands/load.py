import os

from django.conf import settings
from django.core.files.storage import default_storage, FileSystemStorage
from django.core.management.base import BaseCommand
from django.core.management import call_command

from menus.models import Menu
from home.models import HomePage
from wagtail.core.models import Site, Page


class Command(BaseCommand):

    help = 'It seeds the database'

    def _create_menus(self):
        if not Menu.objects.filter(slug='navbar').exists():
            navbar = Menu(title='Navbar', slug='navbar')
            navbar.save()
        if not Menu.objects.filter(slug='footer').exists():
            footer = Menu(title='Footer', slug='footer')
            footer.save()

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
            home = HomePage.objects.get(slug='new_home').update(slug='home')
            home.save()
           

    def handle(self, *args, **options):
        self._delete_wagtail()
        self._create_menus()

    print("Seeded database")
