from curses import panel

from importlib_metadata import MetadataPathFinder
from django_sass import compile_sass, find_static_paths
import os
from django.core.management import call_command

from django.db import models
from django.conf import settings
from wagtail.snippets.models import register_snippet

from wagtail.admin.edit_handlers import MultiFieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting

from wagtail.images.edit_handlers import ImageChooserPanel
from wagtailitalia.settings.base import STATIC_URL
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel


from themes import blocks


@register_snippet
class Theme(models.Model):
    """Wrapper class to provide the other setting classes with some common methods"""
    
    content = StreamField(
        [
            ("color", blocks.Color()),
            ("font", blocks.Font()),
            ("navbar", blocks.Navbar()),
            ("footer", blocks.Navbar()),

        ],
        null=True,
        blank=True
    )    

    panels = [
        StreamFieldPanel("content"),
        ]

    
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


