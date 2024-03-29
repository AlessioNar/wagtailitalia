from django_sass import compile_sass, find_static_paths
from django.core.management import call_command

from django.db import models
from django.conf import settings
from wagtail.snippets.models import register_snippet

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting

from wagtailitalia.settings.base import STATIC_URL


@register_setting
class SocialMediaSettings(BaseSiteSetting):
    """Social media settings for the website"""

    linkedin = models.URLField(blank=True, null=True, help_text="LinkedIn URL")
    github = models.URLField(blank=True, null=True, help_text="Github URL")
    twitter = models.URLField(blank=True, null=True, help_text="Twitter URL")

    panels = [
        MultiFieldPanel([
            FieldPanel("linkedin"),
            FieldPanel("github"),
            FieldPanel("twitter"),
        ], heading="Social Media Settings"),
    ]


@register_setting
class BrandSettings(BaseSiteSetting):
    """Brand settings for the website"""

    brand_name = models.CharField(
        blank=False, null=True, help_text="Brand Name", max_length=250)
    brand_image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )
    brand_subtitle = models.CharField(
        blank=True, null=True, help_text="A subtitle, optional", max_length=300)

    brand_website = models.URLField(
        blank=False, null=False, help_text="Brand URL")
    copyright = models.CharField(
        blank=True, null=False, help_text="Copyright", max_length=250, default='Built with Wagtailitalia')
    
    funding_image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )

    panels = [
        MultiFieldPanel([
            FieldPanel('brand_name'),
            FieldPanel('brand_subtitle'),
            FieldPanel('brand_image'),
            FieldPanel('brand_website'),
            FieldPanel('copyright'),
            FieldPanel('funding_image'),
        ])
     
        
    ]

@register_setting
class AnalyticsSettings(BaseSiteSetting):
    """Analytics settings for the website"""

    google_analytics_id = models.CharField(
        blank=True, null=True, help_text="Google Analytics ID", max_length=250)

    panels = [
        MultiFieldPanel([
            FieldPanel('google_analytics_id'),
        ])
    ]