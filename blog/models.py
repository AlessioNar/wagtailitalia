from django.db import models

from django_extensions.db.fields import AutoSlugField

from django import forms
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from modelcluster.fields import ParentalManyToManyField

from wagtail.admin.edit_handlers import FieldPanel, FieldPanel, MultiFieldPanel

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField

from wagtail.contrib.routable_page.models import RoutablePageMixin

from wagtail.snippets.models import register_snippet

from streams import blocks

from django.contrib.contenttypes.models import ContentType


class BlogTag(models.Model):
    """Blog tag for a snippet"""
    name = models.CharField(max_length=255)
    slug = AutoSlugField(
        populate_from=["name"], editable=True,
        help_text='A slug to identify posts by this tag',

    )

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]

    class Meta:
        verbose_name = "Blog Tag"
        verbose_name_plural = "Blog Tags"
        ordering = ["name"]

    def __str__(self):
        """String Wrapper of this class"""
        return self.name


register_snippet(BlogTag)


class BlogCategory(models.Model):
    """Blog category for a snippet"""
    name = models.CharField(max_length=255)
    slug = AutoSlugField(
        populate_from=["name"], editable=True,
        help_text='A slug to identify posts by this category',

    )

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]

    class Meta:
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"
        ordering = ["name"]

    def __str__(self):
        """String Wrapper of this class"""
        return self.name


register_snippet(BlogCategory)


class Country(models.Model):
    """Country for a snippet"""
    name = models.CharField(max_length=255)
    slug = AutoSlugField(
        populate_from=["name"], editable=True,
        help_text='A slug to identify posts by this country',

    )

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"
        ordering = ["name"]

    def __str__(self):
        """String Wrapper of this class"""
        return self.name

register_snippet(Country)


class BlogDetailPage(Page):
    """Parental Blog Detail Page."""

    template = "blog/blog_detail_page.html"
    custom_title = models.CharField(max_length=100, blank=True, null=True,
                                    help_text="Fill in if you want to change the title on the top of the page")
    category = models.ForeignKey(
        "blog.BlogCategory",
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )

    tags = ParentalManyToManyField(BlogTag, blank=True)

    card_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        related_name="+",
        on_delete=models.SET_NULL,
        help_text="Image used for the card view, suggested 514 × 342 px",
    )

    heading_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        related_name="+",
        on_delete=models.SET_NULL,
        help_text="Image used as a banner, suggested 1200 × 400 px",

    )

    intro = RichTextField(
        blank=True,
        null=True,
        help_text='Intro text for preview'
    )

    content = StreamField(
        [
            ("title", blocks.TitleBlock()),
            ("richtext", blocks.RichtextBlock()),
            ("vertical_card", blocks.VerticalCardBlock()),
            ("horizontal_card", blocks.HorizontalCardBlock()),
            ("multiple_vertical_card_block", blocks.MultipleVerticalCardBlocks()),
            ("multiple_buttons_block", blocks.CardMultipleButtonBlock()),
            ("free_card", blocks.FreeVerticalCardsBlock()),
            ("cta", blocks.CTABlock()),
            ("image", blocks.ImageBlock()),
            ("markdown", blocks.BodyBlock()),
            ("video", blocks.VideoBlock()),

        ],
        null=True,
        blank=True,
        use_json_field=True,

        )
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("custom_title"),
            FieldPanel("intro"),
            FieldPanel("card_image"),
            FieldPanel("heading_image"),
            FieldPanel("category"),
            #FieldPanel("tags", widget=forms.CheckboxSelectMultiple),
        ]),
        FieldPanel("content"),
    ]


class NewsDetailPage(BlogDetailPage):

    """Model for News, the last five of them go in the home page"""
    template = "blog/news_detail_page.html"

    content_panels = BlogDetailPage.content_panels


class ProjectDetailPage(BlogDetailPage):

    """Model for Projects"""
    template = "blog/project_detail_page.html"
    call_id = models.CharField(
        max_length=150, blank=True, null=True, help_text='The call won by the project')
    start_date = models.DateField(
        blank=True, null=True, help_text='The starting date of the project')
    end_date = models.DateField(
        blank=True, null=True, help_text='The end date of the project')
    is_active = models.BooleanField(
        blank=False, null=False, default=True, help_text="The status of the project")

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("custom_title"),
            FieldPanel("intro"),
            FieldPanel("call_id"),
            FieldPanel("card_image"),
            FieldPanel("heading_image"),
            FieldPanel("start_date"),
            FieldPanel("end_date"),
            FieldPanel("is_active"),
            FieldPanel("tags", widget=forms.CheckboxSelectMultiple),
            FieldPanel("category"),
        ]),
        FieldPanel("content"),
    ]


class EventDetailPage(BlogDetailPage):

    """Model for Projects"""
    template = "blog/event_detail_page.html"
    start_date = models.DateField(
        blank=True, null=True, help_text='The starting date of the event')
    end_date = models.DateField(
        blank=True, null=True, help_text='The end date of the project')
    location = models.CharField(
        max_length=200, blank=True, null=True, help_text="Where is the event taking place")
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("custom_title"),
            FieldPanel("intro"),
            FieldPanel("location"),
            FieldPanel("card_image"),
            FieldPanel("heading_image"),
            FieldPanel("start_date"),
            FieldPanel("end_date"),
            FieldPanel("category"),
            FieldPanel("tags", widget=forms.CheckboxSelectMultiple),
        ]),
        FieldPanel("content"),
    ]

class PartnerDetailPage(BlogDetailPage):
    """Partner Detail Page"""

    template = "blog/partner_detail_page.html"
    country = models.ForeignKey(
        "blog.Country",
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )

    website = models.URLField(blank=True, null=True)

    description = RichTextField(
        blank=True,
        null=True,
        help_text='Intro text for preview'
    )
    content_panels = BlogDetailPage.content_panels +  [
            MultiFieldPanel([
                FieldPanel("description"),
                FieldPanel("country"),
                FieldPanel("website"),
            ], heading="Partner Details"),
        ]         


    class Meta:
        verbose_name = "Partner detail Page"
        verbose_name_plural = "Partner detail Pages"



class BlogListingPage(RoutablePageMixin, Page):
    """Listing Page lists all the Blog Detail Pages"""

    template = "blog/blog_listing_page.html"

    heading = models.CharField(max_length=200, blank=True, null=True)

    heading_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
        help_text="Image used as a banner, optional, suggested 1200 × 400 px",

    )

    intro  = RichTextField(blank=True, null=True, help_text="Optional, it will appear above the listing")

    category = models.ForeignKey(
        "blog.BlogCategory",
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    content = StreamField(
        [
            ("title", blocks.TitleBlock()),
            ("richtext", blocks.RichtextBlock()),
            ("vertical_card", blocks.VerticalCardBlock()),
            ("horizontal_card", blocks.HorizontalCardBlock()),
            ("multiple_vertical_card_block", blocks.MultipleVerticalCardBlocks()),
            ("multiple_buttons_block", blocks.CardMultipleButtonBlock()),
            ("free_card", blocks.FreeVerticalCardsBlock()),
            ("cta", blocks.CTABlock()),
            ("image", blocks.ImageBlock()),
            ("markdown", blocks.BodyBlock()),
            ("video", blocks.VideoBlock()),

        ],
        null=True,
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("heading"),
            FieldPanel("heading_image"),
            FieldPanel("intro"),
            FieldPanel("category"),
        ], heading="General Information"),
        FieldPanel("content"),
    ]

    # Category determines the filter for the listing page
    def get_context(self, request, *args, **kwargs):
        """Adding custom elements to our context"""

        context = super().get_context(request, *args, **kwargs)

        # Checks if there are countries associated with partners
        if len(Country.objects.all()) > 0:
            if self.get_children().type(PartnerDetailPage):
                partner_pages = self.get_children().type(PartnerDetailPage).live().public()
                
                partner_pages = PartnerDetailPage.objects.live().public().filter(id__in=partner_pages).order_by('path')
                countries = []
                for page in partner_pages:
                    countries.append(page.country)
                # sort by value and remove duplicates
                countries = sorted(set(countries), key=lambda x: x.name)            
                context['countries'] = countries         
        
        # Check if there is a category filter
        if self.category is not None:
            # Check if there are tags in the URL 
            if request.GET.get('tags'):
                context['tag'] = request.GET.get('tags')                
                # Check if there is a country filter
                if request.GET.get('country'):
                    all_posts = PartnerDetailPage.objects.live().public().filter(country__slug__in=[request.GET.get('country')]).order_by('-path')
                # if there is not, just filter by tags
                else:
                    all_posts = BlogDetailPage.objects.live().public().filter(
                        category=self.category).filter(tags__slug__in=[request.GET.get('tags')]).order_by('path')        
            # If there are no tags, check if there is a country filter
            else:
                # Filter by country
                if request.GET.get('country'):
                    context['country'] = request.GET.get('country')
                    all_posts = PartnerDetailPage.objects.live().public().filter(country__slug__in=[request.GET.get('country')]).order_by('-path')
                # If there is not, just filter by category
                else:                
                    all_posts = BlogDetailPage.objects.live(
                        ).public().filter(category=self.category).order_by('path')
        else:            
            # Take all the posts
            all_posts = BlogDetailPage.objects.live().public().order_by('path')

        # Create a paginator object
        paginator = Paginator(all_posts, 12)        
        # Get the page number from the URL
        page = request.GET.get('page')
        
        # Get the posts for the current page
        try:
            posts = paginator.page(page)
        # If the page is not an integer, deliver the first page
        except PageNotAnInteger:
            posts = paginator.page(1)
        # If the page in the url is empty, deliver the first page
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        
        context['elements'] = posts

        return context
    
    # Creates a route for the sitemap
    def get_sitemap_urls(self, request):
        sitemap = super().get_sitemap_urls(request)
        return sitemap


class HorizontalListingPage(BlogListingPage):
    """Partner Listing Page"""
    template = "blog/horizontal_listing_page.html"
    content_panels = BlogListingPage.content_panels

