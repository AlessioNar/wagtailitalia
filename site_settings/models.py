from django_sass import compile_sass, find_static_paths
import os
from django.core.management import call_command

from django.db import models
from django.conf import settings

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting

from wagtail.images.edit_handlers import ImageChooserPanel


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

    panels = [
        MultiFieldPanel([
            FieldPanel('brand_name'),
            FieldPanel('brand_subtitle'),
            ImageChooserPanel('brand_image'),
            FieldPanel('brand_website')

        ])

    ]


@register_setting
class FundingSettings(BaseSetting):
    """It controls the logo at the bottom of all pages"""

    funding_image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="+",
    )
    panels = [
        ImageChooserPanel('funding_image'),
    ]


@register_setting
class ThemesSettings(BaseSetting):
    """Theme support for wagtailitalia CMS"""
    darktheme = models.BooleanField(default=False, help_text="Tick to set up the dark theme",  verbose_name="Dark Theme")
    
    primary = models.CharField(max_length=7, default="#AAAAAA",
                               help_text="Primary color code, the main color used for your theme")
    secondary = models.CharField(max_length=7, default="#DDDDDD",
                                 help_text="Primary color code, the main color used for your theme")
    light = models.CharField(max_length=7, default="#FFFFFF",
                             help_text="Light color code, used in some backgrounds and text")
    dark = models.CharField(max_length=7, default="#000000",
                            help_text="Dark color code, used in some backgrounds and text")
    blue = models.CharField(max_length=7, default="#000000",
                            help_text="Blue color code, used in some backgrounds and text")
    white = models.CharField(max_length=7, default="#FFFFFF",
                             help_text="White color code, used in some backgrounds and text")
    
    # Make some variables matching the Font settings panel
    font_family = models.CharField(
        blank=True, null=True, help_text="Font family", max_length=250, default='Open+Sans')
    font_size = models.CharField(
        blank=True, null=True, help_text="Font size", max_length=250)
    font_weight = models.CharField(
        blank=True, null=True, help_text="Font weight", max_length=250)
    font_style = models.CharField(
        blank=True, null=True, help_text="Font style", max_length=250)
 
    navbar = models.IntegerField(
        blank=True, null=True, help_text="Navbar height")
    footer = models.IntegerField(
        blank=True, null=True, help_text="Footer height")
    header = models.IntegerField(
        blank=True, null=True, help_text="Header height")


    css = models.TextField(
        blank=True, help_text="Add custom css", default='')

    panels = [
        MultiFieldPanel([
            FieldPanel("darktheme"),
        ], heading="General settings"),
        
        MultiFieldPanel([
            FieldPanel("primary"),
            FieldPanel("secondary"),
            FieldPanel("light"),
            FieldPanel("dark"),
            FieldPanel("white"),
            FieldPanel("blue")
        ], heading="Color settings"),
        
        #MultiFieldPanel([
        #    FieldPanel("cards"),

        #], heading="Cards settings"),
        
        MultiFieldPanel([
            FieldPanel("navbar"),
            FieldPanel("footer"),
            FieldPanel("header"),
        ], heading="Layout settings"), 

        MultiFieldPanel([
            FieldPanel("css"),
        ], heading="Custom CSS"),
       
        # Create a panel for managing the text theme settings in bootstrap4
        MultiFieldPanel([
            FieldPanel("font_family"),
            FieldPanel("font_size"),
            FieldPanel("font_weight"),
            FieldPanel("font_style"),
        ], heading="Font settings"),

            
    ]

    def save(self, *args, **kwargs):
        NAME = settings.NAME
        with open(NAME + '/static/scss/' + NAME + '/' + NAME + '.scss', 'w+') as f:
            # Define scss variables
            print(f'$primary: {self.primary} !default;', file=f)
            print(f'$secondary: {self.secondary} !default;', file=f)
            print(f'$dark: {self.dark} !default;', file=f)
            print(f'$light: {self.light} !default;', file=f)
            print(f'$white: {self.white} !default;', file=f)
            print(f'$blue: {self.blue} !default;', file=f)
            #print(f'$font_family: {self.font_family};', file=f)
            
            print(
                '@import url("https://fonts.googleapis.com/css2?family='+ self.font_family + ':ital,wght,@0,200;0,300;0,400;0,500;0,600;0,700;1,100&display=swap");', file=f)            

            # Define imports
            print(
                "@import '" + NAME + "/static/scss/bootswatch/_variables.scss';", file=f)
            print(
                "@import '" + NAME + "/static/scss/bootstrap/bootstrap.scss';", file=f)
            print(
                "@import '" + NAME + "/static/scss/bootswatch/_bootswatch.scss';", file=f)
            
            print("""
                    * { 
                        font-family: '""" + self.font_family + """' , sans-serif;
                        
                    }
                """, file=f)

            # Add field for custom css
            print(self.css, file=f)

            # Compile scss and write to output file.
        compile_sass(
            inpath=NAME + '/static/scss/'
            + NAME + '/' + NAME + ".scss",
            outpath=NAME + '/static/css/'
            + NAME + '/' + NAME + ".css",
            output_style="compressed",
            precision=8,
            source_map=True
        )

        # Save in database
        super(ThemesSettings, self).save(*args, **kwargs)

        # checking whether file exists or not
        if os.path.exists(r'static/css/' + NAME + '/' + NAME + '.css'):
            # removing the main css file
            os.remove(r'static/css/' + NAME
                      + '/' + NAME + '.css')
        else:
            # file not found message
            print("CSS directory not found")

        # Call Collectstatic original method from manage.py
        call_command('collectstatic', '--no-input')

# Add a class as a snippet to control the main colors used in bootstrap4
class ColorSettings():
    pass