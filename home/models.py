from django.db import models
from django.shortcuts import render
from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel, StreamFieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel

from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from streams import blocks

from blog.models import BlogDetailPage, NewsDetailPage


class HomePage(RoutablePageMixin, Page):
    """Home page model"""

    template = "home/home_page.html"
    max_count = 1
    image = models.ForeignKey(
		"wagtailimages.Image",
		on_delete=models.SET_NULL,
		null=True,
		blank=False,
		related_name="+",
        help_text="Suggested size: 640x420"
		)

    content = StreamField(
        [

            ("title", blocks.TitleBlock()),
            ("richtext", blocks.RichtextBlock()),
            ("vertical_card", blocks.VerticalCardBlock()),
            ("horizontal_card", blocks.HorizontalCardBlock()),
            ("multiple_vertical_card_block", blocks.MultipleVerticalCardBlocks()),
            ("cta", blocks.CTABlock()),
            ("image", blocks.ImageBlock()),
            ("markdown", blocks.BodyBlock()),
            ("jumbotron", blocks.JumbotronBlock()),
        ],
        null=True,
        blank=True
    )

    content_panels = Page.content_panels + [
        ImageChooserPanel("image"),
        StreamFieldPanel("content"),

    ]

    def get_context(self, request, *args, **kwargs):
        """Adding the four latest posts"""
        context = super().get_context(request, *args, **kwargs)
        context["carousel"] = NewsDetailPage.objects.live().public()[:3]
        return context

    class Meta:

        verbose_name = "Home Page"
        verbose_name_plural = "Home Pages"

    @route(r'^subscribe/$')
    def the_subscribe_page(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        return render(request, "home/subscribe.html", context)
