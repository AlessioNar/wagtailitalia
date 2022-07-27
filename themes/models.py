from rest_framework import serializers
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
from django.forms import ModelChoiceField

class Color(models.Model):
    """A Color object containing a name and a color code"""
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255) 

    def __str__(self):
        return self.name                 

register_snippet(Color)

@register_setting
class Theme(BaseSetting):
    """Wrapper class to provide the other setting classes with some common methods"""
    
    primary = models.ForeignKey(Color, related_name="primary", null=True, on_delete=models.SET_NULL)    
    secondary = models.ForeignKey(Color, related_name="secondary", null=True, on_delete=models.SET_NULL)    
    dark = models.ForeignKey(Color, related_name="dark", null=True, on_delete=models.SET_NULL)    
    light = models.ForeignKey(Color, related_name="light", null=True, on_delete=models.SET_NULL)    
    danger = models.ForeignKey(Color, related_name="danger", null=True, on_delete=models.SET_NULL)    
    success = models.ForeignKey(Color, related_name="success", null=True, on_delete=models.SET_NULL)    
    warning = models.ForeignKey(Color, related_name="warning", null=True, on_delete=models.SET_NULL)

    font_color = models.ForeignKey(Color, related_name="font_color", null=True, on_delete=models.SET_NULL)    
    font_size = models.IntegerField(default=16, help_text="Font size in px")
    font_family = models.CharField(max_length=255, default="Montserrat", 
        help_text="Choose a Google font family")        

    nav_title_size = models.IntegerField(default=16, help_text="Font size in px")
    nav_bg_color = models.ForeignKey('themes.Color', related_name="navbar_bg_color", on_delete=models.SET_NULL, null=True, blank=True)
    nav_text_color = models.ForeignKey('themes.Color', related_name="navbar_text_color", on_delete=models.SET_NULL, null=True, blank=True)
    nav_subtitle_size = models.IntegerField(default=11, help_text="Font size in px")
    nav_subtitle_show = models.BooleanField(default=True)
    dark_background_color = models.BooleanField(default=False)

    car_title_size = models.IntegerField(default=16, help_text="Font size in px")
    car_bg_color = models.ForeignKey('themes.Color', related_name="car_bg_color", on_delete=models.SET_NULL, null=True, blank=True)
    

    foot_bg_color = models.ForeignKey('themes.Color', related_name="footer_bg_color", on_delete=models.SET_NULL, null=True, blank=True)
    foot_text_color = models.ForeignKey('themes.Color', related_name="footer_text_color", on_delete=models.SET_NULL, null=True, blank=True)
    foot_text_size = models.IntegerField(default=16, help_text="Font size in px")    

    jumbo_bg_color = models.ForeignKey('themes.Color', related_name="jumbotron_bg_color", on_delete=models.SET_NULL, null=True, blank=True)
    jumbo_text_color = models.ForeignKey('themes.Color', related_name="jumbotron_text_color", on_delete=models.SET_NULL, null=True, blank=True)
    jumbo_title_size = models.IntegerField(default=16, help_text="Font size in px")
    jumbo_button_color = models.ForeignKey('themes.Color', on_delete=models.SET_NULL, null=True, blank=True)
    jumbo_button_size = models.IntegerField(default=14, help_text="Button size in rem")
        
   
    panels = [        
        MultiFieldPanel([
            FieldPanel("primary"),
            FieldPanel("secondary"),
            FieldPanel("dark"),
            FieldPanel("light"),
            FieldPanel("danger"),
            FieldPanel("success"),
            FieldPanel("warning"),
        ], "Colors"),

        MultiFieldPanel([
            FieldPanel('font_color'),
            FieldPanel('font_size'),
            FieldPanel('font_family'),
        ], heading="Font"),

        MultiFieldPanel([
            FieldPanel('nav_title_size'),
            FieldPanel('nav_bg_color'),
            FieldPanel('dark_background_color'),
            FieldPanel('nav_text_color'),
            FieldPanel('nav_subtitle_size'),
            FieldPanel('nav_subtitle_show'),            
        ], heading="Navbar"),

        MultiFieldPanel([
            FieldPanel('car_title_size'),
            FieldPanel('car_bg_color'),
        ], heading="Carousel"),

        MultiFieldPanel([
            FieldPanel('jumbo_bg_color'),
            FieldPanel('jumbo_text_color'),
            FieldPanel('jumbo_title_size'),
            FieldPanel('jumbo_button_color'),
            FieldPanel('jumbo_button_size'),
        ], heading="Jumbotron"),

        MultiFieldPanel([
            FieldPanel('foot_bg_color'),
            FieldPanel('foot_text_color'),
            FieldPanel('foot_text_size'),
        ], heading="Footer"),
        
        ]

    class Meta:                
        verbose_name = "Theme Settings"

    ## A function that uses the values stored in the model to print to a file the corresponding Boostrap SCSS variables
    def print_scss(self):
        """Prints the SCSS variables contained in the model to a file, color, font and navbar"""
        NAME = settings.NAME
        with open(os.path.join(NAME, "static/scss/themes/theme.scss"), "w") as f:
            
            f.write("$primary: " + self.primary.code + ";\n")            
            f.write("$secondary: " + self.secondary.code + ";\n")            
            f.write("$success: " + self.success.code + ";\n")            
            f.write("$warning: " + self.warning.code + ";\n")
            f.write("$danger: " + self.danger.code + ";\n")
            f.write("$light: " + self.light.code + ";\n")
            f.write("$dark: " + self.dark.code + ";\n")            

            f.write("$font-family-sans-serif: " + self.font_family + ";\n")            
            f.write("$font-size-base: " + str(self.font_size * 0.0625) + "rem ;\n")
            f.write("$font-color: " + self.font_color.code + ";\n")
            
            f.write("$navbar-brand-font-size: " + str(self.nav_title_size * 0.0625) + "rem ;\n")
            f.write("$navbar-subtitle-size: " + str(self.nav_subtitle_size * 0.0625) + "rem ;\n")
            f.write("$navbar-bg-color: " + self.nav_bg_color.code + ";\n")
            """
            f.write("$navbar-bg-color: " + self.navbar.bg_color + ";\n")
            f.write("$navbar-text-color: " + self.navbar.text_color + ";\n")            
            f.write("$navbar-subtitle-show: " + self.navbar.subtitle_show + ";\n")
            """
            f.write("$carousel-bg-color: " + self.car_bg_color.code + ";\n")
            f.write("$carousel-font-size: " + str(self.car_title_size * 0.0625) + "rem;\n")
            
            f.write("$jumbotron-bg-color: " + self.jumbo_bg_color.code + ";\n")
            f.write("$jumbotron-text-color: " + self.jumbo_text_color.code + ";\n")

            """            
            f.write("$footer-bg-color: " + self.footer.bg_color + ";\n")
            f.write("$footer-text-color: " + self.footer.text_color + ";\n")
            f.write("$footer-subtitle-size: " + self.footer.subtitle_size + ";\n")
            f.write("$footer-subtitle-show: " + self.footer.subtitle_show + ";\n")
            f.write("$footer-title-size: " + self.footer.title_size + ";\n")
            
            f.write("$jumbotron-button-color: " + self.jumbotron.button_color + ";\n")
            f.write("$jumbotron-button-size: " + self.jumbotron.button_size + ";\n")
            """

            f.write("@import 'wagtailitalia/static/scss/bootswatch/_variables';\n")
            f.write("@import 'wagtailitalia/static/scss/bootstrap/bootstrap';\n")
            f.write("@import 'wagtailitalia/static/scss/bootswatch/bootswatch';\n")

            f.write(".navbar-brand-subtitle{\nfont-size: $navbar-subtitle-size\n}\n")
            f.write(".navbar{\nbackground-color: $navbar-bg-color\n}\n")
            f.write(".dropdown-menu{\nbackground-color: $navbar-bg-color\n}\n")      
            f.write(".carousel-caption {\nposition: inherit;\n}\n")
            f.write(".carousel-home{\nbackground-color: $carousel-bg-color;\nheight:auto;\n}\n")
            f.write(".jumbotron{\nbackground-color: $jumbotron-bg-color;\ncolor: $jumbotron-text-color;\n}\n")

            f.write(".card-title, .card-header {\nheight: 5em;\ntext-align: center;\n line-height: 1.8em;\n}\n")
            f.write(".card {\nborder: none;\nheight: 20em;\n}\n")
            f.write(".card-item {\nbox-shadow: rgba(0, 0, 0, 0.25) 0px 54px 55px, rgba(0, 0, 0, 0.12) 0px -12px 30px, rgba(0, 0, 0, 0.12) 0px 4px 6px, rgba(0, 0, 0, 0.17) 0px 12px 13px, rgba(0, 0, 0, 0.09) 0px -3px 5px;\n}\n")

        

    
    def compile_scss(self):
        """Compile the scss file and write the output to the css file"""

        NAME = settings.NAME

        # Compile the SCSS file into the CSS file
        compile_sass(
            inpath=os.path.join(NAME,'static/scss/themes/theme.scss'),
            outpath=os.path.join(NAME, 'static/css/themes/theme.css'),
            output_style="compressed",
            precision=8,
            source_map=True
        )
        
        # If the file already exist, remove the previous file and replace it with the new one
        if os.path.exists(os.path.join('static/css/themes/theme.css')):
            # Remove the previous file
            os.remove(os.path.join('static/css/themes/theme.css'))
        else:
            # Print a message if the file doesn't exist
            print("CSS directory not found")

        # Collect the new static files
        call_command('collectstatic', '--no-input')

    def save(self, *args, **kwargs):
        """Override the save method to compile the scss file"""
        self.print_scss()
        self.compile_scss()
        super(Theme, self).save(*args, **kwargs)
