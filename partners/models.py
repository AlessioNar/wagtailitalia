from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel

from wagtail.core.models import Orderable, Page

from wagtail.images.edit_handlers import ImageChooserPanel

from blog.models import BlogDetailPage, ProjectDetailPage
from modelcluster.fields import ParentalKey


class PartnerDetailPage(BlogDetailPage):
    """Partner Detail Page"""

    template = "blog/partner_detail_page.html"

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("intro"),
            FieldPanel("website"),
            FieldPanel("category"),
            ImageChooserPanel("card_image"),
            ImageChooserPanel("heading_image"),
        ]),
        StreamFieldPanel("content"),


    ]

    class Meta:
        abstract = True
        verbose_name = "Partner"
        verbose_name_plural = "Partners"


class ProjectDetailPagePartnerDetailPage(Orderable, ProjectDetailPage):
    page = ParentalKey('blog.ProjectDetailPage', on_delete=models.SET_NULL,
                       related_name='partners')
