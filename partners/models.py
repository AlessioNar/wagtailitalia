from blog.models import BlogDetailPage, BlogListingPage
from django.db import models
from django_extensions.db.fields import AutoSlugField


from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.snippets.models import register_snippet

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

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

class PartnerDetailPage(BlogDetailPage):
    """Partner Detail Page"""

    template = "partners/partner_detail_page.html"
    country = models.ForeignKey(
        "partners.Country",
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


class PartnerListingPage(BlogListingPage):
    """Partner Listing Page lists all the PartnerDetailPages and provide a way to filter them"""
    template = "partners/partner_listing_page.html"
    content_panels = BlogListingPage.content_panels

    # Category determines the filter for the listing page
    def get_context(self, request, *args, **kwargs):        
        """Filters the partner listing page by the country selected"""
        
        context = super().get_context(request, *args, **kwargs)
        if request.GET.get('country'):
            context['country'] = request.GET.get('country')
            all_posts = PartnerDetailPage.objects.live().public().filter(
                country__slug=context['country']).order_by('path')
            paginator = Paginator(all_posts, 12) 
            page = request.GET.get('page')
            try:
                posts = paginator.page(page)
            except PageNotAnInteger:
                posts = paginator.page(1)
            except EmptyPage:
                posts = paginator.page(paginator.num_pages)
            context['elements'] = posts               
        else:            
            all_posts = PartnerDetailPage.objects.live().public().order_by('path')            
            paginator = Paginator(all_posts, 12)
            page = request.GET.get('page')
            try:
                posts = paginator.page(page)
            except PageNotAnInteger:
                posts = paginator.page(1)
            except EmptyPage:
                posts = paginator.page(paginator.num_pages)

            context['elements'] = posts

        return context