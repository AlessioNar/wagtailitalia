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
    
    # Save function to update the css file
    def save(self, *args, **kwargs):
        NAME = settings.NAME
        scss_file = os.path.join(settings.PROJECT_DIR, "static/scss/", settings.NAME, settings.NAME + ".scss")

        with open(scss_file, "w") as f:            
            #f.write('@import url("https://fonts.googleapis.com/css2?family=%s:ital,wght,@0,200;0,300;0,400;0,500;0,600;0,700;1,100&display=swap");\n' % self.font_family)
            f.write("@import '%s/static/scss/wagtailitalia/colors.scss';\n" % NAME)
            f.write("@import '%s/static/scss/wagtailitalia/navbar';\n" % NAME)

            #f.write("@import '%s/static/scss/bootswatch/_variables.scss';\n" % NAME)

            f.write("@import '%s/static/scss/bootstrap/functions';\n" % NAME)
            f.write("@import '%s/static/scss/bootstrap/variables';\n" % NAME)              
            f.write("@import '%s/static/scss/bootstrap/mixins';\n" % NAME)               
                            
            f.write("@import '%s/static/scss/bootstrap/buttons';\n" % NAME)
            f.write("@import '%s/static/scss/bootstrap/button-group';\n" % NAME)
            
            f.write("@import '%s/static/scss/bootstrap/card';\n" % NAME)
            f.write("@import '%s/static/scss/bootstrap/carousel';\n" % NAME)
            f.write("@import '%s/static/scss/bootstrap/close';\n" % NAME)
            f.write("@import '%s/static/scss/bootstrap/containers';\n" % NAME)
            f.write("@import '%s/static/scss/bootstrap/dropdown';\n" % NAME)
            f.write("@import '%s/static/scss/bootstrap/grid';\n" % NAME)
        
            f.write("@import '%s/static/scss/bootstrap/helpers';\n" % NAME)
            f.write("@import '%s/static/scss/bootstrap/images';\n" % NAME)
            f.write("@import '%s/static/scss/bootstrap/list-group';\n" % NAME)

            f.write("@import '%s/static/scss/bootstrap/nav';\n" % NAME)
            f.write("@import '%s/static/scss/bootstrap/navbar';\n" % NAME)

            f.write("@import '%s/static/scss/bootstrap/offcanvas';\n" % NAME)
            f.write("@import '%s/static/scss/bootstrap/reboot';\n" % NAME)
            f.write("@import '%s/static/scss/bootstrap/root';\n" % NAME)

            f.write("@import '%s/static/scss/bootstrap/transitions';\n" % NAME)
            f.write("@import '%s/static/scss/bootstrap/type';\n" % NAME)
            

            f.write("@import '%s/static/scss/bootstrap/utilities';\n" % NAME)
            f.write("@import '%s/static/scss/bootstrap/bootstrap-grid';\n" % NAME)
            f.write("@import '%s/static/scss/bootstrap/bootstrap-utilities';\n" % NAME)
                        
            #f.write("@import '%s/static/scss/bootswatch/_bootswatch.scss';\n" % NAME)                                        

            f.write("@import '%s/static/scss/wagtailitalia/jumbotron';\n" % NAME)            
            f.write(self.css)
                
            # Save the 
            super(ThemeSetting, self).save(*args, **kwargs)
            # Compile scss and write to output file.

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

