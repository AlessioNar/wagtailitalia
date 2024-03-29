from importlib.resources import path
import os
import json
from unicodedata import category

from django.conf import settings
from django.core.files.storage import default_storage, FileSystemStorage
from django.core.management.base import BaseCommand
from django.core.management import call_command

from home.models import HomePage
from menus.models import Menu, MenuItem, SubmenuItem
from blog.models import BlogCategory, BlogListingPage, NewsDetailPage, ProjectDetailPage, EventDetailPage, BlogDetailPage # noqa

from wagtail.images.models import Image

from wagtail.core.models import Site, Page


class Command(BaseCommand):

    help = 'It seeds the database'

    def _delete_wagtail(self):

        if Page.objects.filter(slug='home').exists():
            
            # Create a new home page
            root_page = Page.objects.get(slug="home").get_parent().specific
            new_home = HomePage(title='Home', slug='new_home',
                                depth=2, path='00010001')
            root_page.add_child(instance=new_home)
            new_home.save()

            # Update the home page in the site model
            site = Site.objects.update(
                root_page=new_home, hostname='localhost')

            # Delete initial home page
            home = Page.objects.get(slug='home')
            home.delete()
            
            # Change the slug of the home page to 'home'
            home = HomePage.objects.get(slug='new_home')
            home.slug = 'home'
            
            home.content = json.dumps([
                {'type':'richtext', 'value': 'Congratulations! Your Wagtailitalia instance is up!'}
            ])
            
            home.save()            

            return
    
    def _create_categories(self):
        
        if not BlogCategory.objects.filter(slug='news').exists():
            cat = BlogCategory(name='News', slug='news')
            cat.save()
        
        if not BlogCategory.objects.filter(slug='events').exists():
            cat = BlogCategory(name='Events', slug='events')
            cat.save()
        
        if not BlogCategory.objects.filter(slug='publications').exists():
            cat = BlogCategory(name='Publications', slug='publications')
            cat.save()
        
        if not BlogCategory.objects.filter(slug='partners').exists():
            cat = BlogCategory(name='Partners', slug='partners')
            cat.save()
        
        if not BlogCategory.objects.filter(slug='results').exists():
            cat = BlogCategory(name='Results', slug='results')
            cat.save()
    
    def _upload_images(self):
        if len(Image.objects.all()) == 0:
            Image(title='image-1', file='original_images/image-1.jpg').save()
            Image(title='image-2', file='original_images/image-2.jpg').save()
            Image(title='image-3', file='original_images/image-3.jpg').save()

    def _create_pages(self):

        # Get the home page 
        home = Page.objects.get(slug="home")
    

        # Create a new blog listing page for news
        newslistingpage = BlogListingPage(title='News', slug='news', heading="News", category=BlogCategory.objects.get(slug='news'))
        home.add_child(instance=newslistingpage)
        newslistingpage.save()
        
        # Create a new blog listing page for events
        eventslistingpage = BlogListingPage(title='Events', slug='events', heading='Events', category=BlogCategory.objects.get(slug='events'))
        home.add_child(instance=eventslistingpage)
        eventslistingpage.save()

        # Create a new blog listing page for publications
        publicationslistingpage = BlogListingPage(title='Publications', slug='publications', heading='Publications', category=BlogCategory.objects.get(slug='publications'))
        home.add_child(instance=publicationslistingpage)
        publicationslistingpage.save()

        # Create a new blog listing page for partners
        partnerslistingpage = BlogListingPage(title='Partners', slug='partners', heading='Partners', category=BlogCategory.objects.get(slug='partners'))
        home.add_child(instance=partnerslistingpage)
        partnerslistingpage.save()

        # Create a new blog listing page for results
        resultslistingpage = BlogListingPage(title='Results', slug='results', heading='Results', category=BlogCategory.objects.get(slug='results'))
        home.add_child(instance=resultslistingpage)
        resultslistingpage.save()

        # Create a contact page
        contactpage = BlogDetailPage(title='Contact', 
                                    slug='contact', 
                                    custom_title='Our team', 
                                    card_image=Image.objects.get(title='image-1'), 
                                    heading_image=Image.objects.get(title='image-2'))

        home.add_child(instance=contactpage)
        contactpage.save()

        home.save()
        return

    def _create_news(self):
        # Get the home page 
        news = Page.objects.get(slug="news")

        # Create a new blog listing page for news
        news_1 = NewsDetailPage(title='Welcome to your Wagtailitalia project!', 
                                slug='news-1',
                                custom_title='Welcome to your Wagtailitalia project!',
                                category = BlogCategory.objects.get(slug='news'),
                                card_image = Image.objects.get(title='image-1'),
                                heading_image = Image.objects.get(title='image-1'),
                                intro = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce et libero sit amet elit faucibus blandit vel sit amet lacus. Integer efficitur, nisl eu scelerisque posuere, mi eros dignissim dolor, ut interdum nisl enim sed dui. Suspendisse maximus risus vel viverra imperdiet.',
                                )
        news.add_child(instance=news_1)
        news_1.save()

        news_2 = NewsDetailPage(title='A second blog post',
                                slug = 'news-2',
                                custom_title='A second blog post',
                                category = BlogCategory.objects.get(slug='news'),
                                card_image = Image.objects.get(title='image-2'),
                                heading_image = Image.objects.get(title='image-2'),
                                intro = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce et libero sit amet elit faucibus blandit vel sit amet lacus. Integer efficitur, nisl eu scelerisque posuere, mi eros dignissim dolor, ut interdum nisl enim sed dui. Suspendisse maximus risus vel viverra imperdiet.',
                                )
        news.add_child(instance=news_2)
        news_2.save()
        
        news_3 = NewsDetailPage(title='A third blog post',
                                slug = 'news-3',
                                custom_title='A third blog post',
                                category = BlogCategory.objects.get(slug='news'),
                                card_image = Image.objects.get(title='image-3'),
                                heading_image = Image.objects.get(title='image-3'),
                                intro = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce et libero sit amet elit faucibus blandit vel sit amet lacus. Integer efficitur, nisl eu scelerisque posuere, mi eros dignissim dolor, ut interdum nisl enim sed dui. Suspendisse maximus risus vel viverra imperdiet.',
                                )
        news.add_child(instance=news_3)
        news_3.save()

        return

  
    def _create_events(self):
        events = Page.objects.get(slug="events")

        event_1 = BlogDetailPage(title='Event 1', 
                                slug = 'event-1',
                                custom_title='A general-purpose event',
                                category = BlogCategory.objects.get(slug='events'),
                                card_image = Image.objects.get(title='image-1'),
                                heading_image = Image.objects.get(title='image-1'),
                                intro = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce et libero sit amet elit faucibus blandit vel sit amet lacus. Integer efficitur, nisl eu scelerisque posuere, mi eros dignissim dolor, ut interdum nisl enim sed dui. Suspendisse maximus risus vel viverra imperdiet.',
                                )
        events.add_child(instance=event_1)
        event_1.save()
        
        event_2 = BlogDetailPage(title='Event 2',
                                slug = 'event-2',
                                custom_title='Another general-purpose event',
                                category = BlogCategory.objects.get(slug='events'),
                                card_image = Image.objects.get(title='image-2'),
                                heading_image = Image.objects.get(title='image-2'),
                                intro = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce et libero sit amet elit faucibus blandit vel sit amet lacus. Integer efficitur, nisl eu scelerisque posuere, mi eros dignissim dolor, ut interdum nisl enim sed dui. Suspendisse maximus risus vel viverra imperdiet.',
                                )
        events.add_child(instance=event_2)
        event_2.save()


        event_3 = BlogDetailPage(title='Event 3',
                                slug = 'event-3',
                                custom_title='A third general-purpose event',
                                category = BlogCategory.objects.get(slug='events'),
                                card_image = Image.objects.get(title='image-3'),
                                heading_image = Image.objects.get(title='image-3'),
                                intro = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce et libero sit amet elit faucibus blandit vel sit amet lacus. Integer efficitur, nisl eu scelerisque posuere, mi eros dignissim dolor, ut interdum nisl enim sed dui. Suspendisse maximus risus vel viverra imperdiet.',
                                )
        events.add_child(instance=event_3)
        event_3.save()
        
        
        return 

    def _create_publications(self):
        publications = Page.objects.get(slug="publications")

        publication_1 = BlogDetailPage(title='Publication 1', 
                                slug = 'publication-1',
                                custom_title='A general-purpose publication',
                                category = BlogCategory.objects.get(slug='publications'),
                                card_image = Image.objects.get(title='image-1'),
                                heading_image = Image.objects.get(title='image-1'),
                                intro = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce et libero sit amet elit faucibus blandit vel sit amet lacus. Integer efficitur, nisl eu scelerisque posuere, mi eros dignissim dolor, ut interdum nisl enim sed dui. Suspendisse maximus risus vel viverra imperdiet.',
                                )
        publications.add_child(instance=publication_1)
        publication_1.save()
        
        publication_2 = BlogDetailPage(title='Publication 2',
                                slug = 'publication-2',
                                custom_title='Another general-purpose publication',
                                category = BlogCategory.objects.get(slug='publications'),
                                card_image = Image.objects.get(title='image-2'),
                                heading_image = Image.objects.get(title='image-2'),
                                intro = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce et libero sit amet elit faucibus blandit vel sit amet lacus. Integer efficitur, nisl eu scelerisque posuere, mi eros dignissim dolor, ut interdum nisl enim sed dui. Suspendisse maximus risus vel viverra imperdiet.',
                                )
        publications.add_child(instance=publication_2)
        publication_2.save()


        publication_3 = BlogDetailPage(title='Publication 3',
                                slug = 'publication-3',
                                custom_title='A third general-purpose publication',
                                category = BlogCategory.objects.get(slug='publications'),
                                card_image = Image.objects.get(title='image-3'),
                                heading_image = Image.objects.get(title='image-3'),
                                intro = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce et libero sit amet elit faucibus blandit vel sit amet lacus. Integer efficitur, nisl eu scelerisque posuere, mi eros dignissim dolor, ut interdum nisl enim sed dui. Suspendisse maximus risus vel viverra imperdiet.',
                                )
        publications.add_child(instance=publication_3)
        publication_3.save()
            
        return 

    def _create_partners(self):
        partners = Page.objects.get(slug="partners")

        partner_1 = BlogDetailPage(title='partner 1', 
                                slug = 'partner-1',
                                custom_title='A general-purpose partner',
                                category = BlogCategory.objects.get(slug='partners'),
                                card_image = Image.objects.get(title='image-1'),
                                heading_image = Image.objects.get(title='image-1'),
                                intro = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce et libero sit amet elit faucibus blandit vel sit amet lacus. Integer efficitur, nisl eu scelerisque posuere, mi eros dignissim dolor, ut interdum nisl enim sed dui. Suspendisse maximus risus vel viverra imperdiet.',
                                )
        partners.add_child(instance=partner_1)
        partner_1.save()
        
        partner_2 = BlogDetailPage(title='partner 2',
                                slug = 'partner-2',
                                custom_title='Another general-purpose partner',
                                category = BlogCategory.objects.get(slug='partners'),
                                card_image = Image.objects.get(title='image-2'),
                                heading_image = Image.objects.get(title='image-2'),
                                intro = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce et libero sit amet elit faucibus blandit vel sit amet lacus. Integer efficitur, nisl eu scelerisque posuere, mi eros dignissim dolor, ut interdum nisl enim sed dui. Suspendisse maximus risus vel viverra imperdiet.',
                                )
        partners.add_child(instance=partner_2)
        partner_2.save()


        partner_3 = BlogDetailPage(title='partner 3',
                                slug = 'partner-3',
                                custom_title='A third general-purpose partner',
                                category = BlogCategory.objects.get(slug='partners'),
                                card_image = Image.objects.get(title='image-3'),
                                heading_image = Image.objects.get(title='image-3'),
                                intro = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce et libero sit amet elit faucibus blandit vel sit amet lacus. Integer efficitur, nisl eu scelerisque posuere, mi eros dignissim dolor, ut interdum nisl enim sed dui. Suspendisse maximus risus vel viverra imperdiet.',
                                )
        partners.add_child(instance=partner_3)
        partner_3.save()
            
        return 

    def _create_results(self):
        results = Page.objects.get(slug="results")

        result_1 = BlogDetailPage(title='result 1', 
                                slug = 'result-1',
                                custom_title='A general-purpose result',
                                category = BlogCategory.objects.get(slug='results'),
                                card_image = Image.objects.get(title='image-1'),
                                heading_image = Image.objects.get(title='image-1'),
                                intro = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce et libero sit amet elit faucibus blandit vel sit amet lacus. Integer efficitur, nisl eu scelerisque posuere, mi eros dignissim dolor, ut interdum nisl enim sed dui. Suspendisse maximus risus vel viverra imperdiet.',
                                )
        results.add_child(instance=result_1)
        result_1.save()
        
        result_2 = BlogDetailPage(title='result 2',
                                slug = 'result-2',
                                custom_title='Another general-purpose result',
                                category = BlogCategory.objects.get(slug='results'),
                                card_image = Image.objects.get(title='image-2'),
                                heading_image = Image.objects.get(title='image-2'),
                                intro = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce et libero sit amet elit faucibus blandit vel sit amet lacus. Integer efficitur, nisl eu scelerisque posuere, mi eros dignissim dolor, ut interdum nisl enim sed dui. Suspendisse maximus risus vel viverra imperdiet.',
                                )
        results.add_child(instance=result_2)
        result_2.save()


        result_3 = BlogDetailPage(title='result 3',
                                slug = 'result-3',
                                custom_title='A third general-purpose result',
                                category = BlogCategory.objects.get(slug='results'),
                                card_image = Image.objects.get(title='image-3'),
                                heading_image = Image.objects.get(title='image-3'),
                                intro = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce et libero sit amet elit faucibus blandit vel sit amet lacus. Integer efficitur, nisl eu scelerisque posuere, mi eros dignissim dolor, ut interdum nisl enim sed dui. Suspendisse maximus risus vel viverra imperdiet.',
                                )
        results.add_child(instance=result_3)
        result_3.save()
            
        return 
    
    def _create_contact(self):
        contact = Page.objects.get(slug="contact")
        contact.content = json.dumps([
                {'type':'horizontal_card', 'title': 'Contact person 1'}
            ])
        contact.save()

    def _create_menus(self):

        # Create a new navbar menu
        if not Menu.objects.filter(slug='navbar').exists():
            navbar = Menu(title='Navbar', slug='navbar')
            navbar.save()
            
            # Create new menu items for the navbar
            navbar = Menu.objects.get(slug='navbar')
            navbar.menu_items.add(MenuItem(link_title='Home', link_page=HomePage.objects.get(slug='home')))
            navbar.menu_items.add(MenuItem(link_title='News & Events'))
            navbar.menu_items.add(MenuItem(link_title='Partners', link_url='/'))
            navbar.menu_items.add(MenuItem(link_title='Results', link_url='/'))
            navbar.menu_items.add(MenuItem(link_title='Synergies', link_url='/'))
            navbar.menu_items.add(MenuItem(link_title='Contact', link_page=BlogDetailPage.objects.get(slug='contact')))
            navbar.save()

            # Create sub-menu items for the navbar
            newsevent = MenuItem.objects.get(link_title='News & Events')
            newsevent.submenu_items.add(SubmenuItem(link_title='News', link_page=BlogListingPage.objects.get(slug='news')))
            newsevent.submenu_items.add(SubmenuItem(link_title='Events', link_page=BlogListingPage.objects.get(slug='events')))
            newsevent.submenu_items.add(SubmenuItem(link_title='Publications', link_page=BlogListingPage.objects.get(slug='publications')))
            newsevent.save()

            partners = MenuItem.objects.get(link_title='Partners')
            partners.submenu_items.add(SubmenuItem(link_title='All Partners', link_page=BlogListingPage.objects.get(slug='partners')))
            partners.submenu_items.add(SubmenuItem(link_title='Partner 1', link_page=BlogDetailPage.objects.get(slug='partner-1')))
            partners.submenu_items.add(SubmenuItem(link_title='Partner 2', link_page=BlogDetailPage.objects.get(slug='partner-2')))
            partners.submenu_items.add(SubmenuItem(link_title='Partner 3', link_page=BlogDetailPage.objects.get(slug='partner-3')))
            partners.save()

            results = MenuItem.objects.get(link_title='Results', link_url='/')
            results.submenu_items.add(SubmenuItem(link_title='All Results', link_page=BlogListingPage.objects.get(slug='results')))
            results.submenu_items.add(SubmenuItem(link_title='Result 1', link_page=BlogDetailPage.objects.get(slug='result-1')))
            results.submenu_items.add(SubmenuItem(link_title='Result 2', link_page=BlogDetailPage.objects.get(slug='result-2')))
            results.submenu_items.add(SubmenuItem(link_title='Result 3', link_page=BlogDetailPage.objects.get(slug='result-3')))
            results.save()

        if not Menu.objects.filter(slug='footer').exists():
            footer = Menu(title='Footer', slug='footer')
            footer.save()

        

        return

    def handle(self, *args, **options):
        self._delete_wagtail()
        self._upload_images()
        self._create_categories()
        self._create_pages()
        self._create_news()        
        self._create_events()
        self._create_publications()
        self._create_partners()     
        self._create_results()
        self._create_contact()
        self._create_menus()


    print("Seeded database")
