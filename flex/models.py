"""Flexible page"""
from django.db import models

from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import StreamField

from streams import blocks


class FlexPage(Page):

    """Flexible page class"""

    template = "flex/flex_page.html"

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
            ("simple_richtext", blocks.SimpleRichtextBlock()),
            ("vertical_card", blocks.VerticalCardBlock()),
            ("horizontal_card", blocks.HorizontalCardBlock()),
            ("cta", blocks.CTABlock()),
            ("button", blocks.ButtonBlock()),
            ("image", blocks.ImageBlock()),
            ("markdown", blocks.BodyBlock()),

        ],
        null=True,
        blank=True
    )

    subtitle = models.CharField(max_length=100, null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        FieldPanel("category"),
        StreamFieldPanel("content"),
    ]

    class Meta:  # noqua
        verbose_name = "Flex Page"
        verbose_name_plural = "Flex Pages"
