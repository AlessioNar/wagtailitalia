from curses import panel

from importlib_metadata import MetadataPathFinder
from django_sass import compile_sass, find_static_paths
import os
from django.core.management import call_command

from django.db import models
from django.conf import settings
from wagtail.snippets.models import register_snippet

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting

from wagtail.images.edit_handlers import ImageChooserPanel
from wagtailitalia.settings.base import STATIC_URL


@register_setting
class SocialMediaSettings(BaseSetting):
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
class BrandSettings(BaseSetting):
    """Brand settings for the website"""

    brand_name = models.CharField(
        blank=False, null=True, help_text="Brand Name", max_length=250)
    brand_image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
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
        blank=False,
        related_name="+",
    )

    panels = [
        MultiFieldPanel([
            FieldPanel('brand_name'),
            FieldPanel('brand_subtitle'),
            ImageChooserPanel('brand_image'),
            FieldPanel('brand_website'),
            FieldPanel('copyright'),
            ImageChooserPanel('funding_image'),
        ])
     
        
    ]


 
class ThemeSetting(BaseSetting):
    """Wrapper class to provide the other setting classes with some common methods"""
    

    def compile_scss(self):
        """Compile the scss file and write the output to the css file"""

        NAME = settings.NAME

        # Compile the SCSS file into the CSS file
        compile_sass(
            inpath=os.path.join(NAME,'static/scss/', NAME, NAME + ".scss"),
            outpath=os.path.join(NAME + 'static/css/', NAME, NAME + ".css"),
            output_style="compressed",
            precision=8,
            source_map=True
        )
        
        # If the file already exist, remove the previous file and replace it with the new one
        if os.path.exists(os.path.join('static/css/', NAME, NAME + '.css')):
            # Remove the previous file
            os.remove(os.path.join('static/css/', NAME, NAME + '.css'))
        else:
            # Print a message if the file doesn't exist
            print("CSS directory not found")

        # Collect the new static files
        call_command('collectstatic', '--no-input')

class ColorSetting(ThemeSetting):    
    primary = models.CharField(max_length=7, default="#FFFFFF",
                               help_text="Primary color for the theme")    

    panels = [
        MultiFieldPanel([
            FieldPanel("primary"),    
        ], heading="Color settings"),
    ]    
        
    class Meta:
        verbose_name = "Color Settings"

@register_setting
class TestSetting(ThemeSetting):
    """Test settings for the website"""

    colors = ColorSetting()

    panels = [
        MultiFieldPanel([
            FieldPanel("colors"),
        ], heading="Test Settings"),
    ]

    class Meta:
        verbose_name = "Test Settings"