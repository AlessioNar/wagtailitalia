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

class ColorPalette(models.Model):   
    """A color palette"""

    name  = models.CharField(max_length=255, blank=True, null=True)

    primary = models.CharField(max_length=7, default="#FFFFFF", 
        help_text="Add an exadecimal color code: #FFFFFF for white")    
    secondary = models.CharField(max_length=7, default="#FFFFFF", 
        help_text="Add an exadecimal color code: #FFFFFF for white")    
    dark = models.CharField(max_length=7, default="#FFFFFF", 
        help_text="Add an exadecimal color code: #FFFFFF for white")    
    light = models.CharField(max_length=7, default="#FFFFFF", 
        help_text="Add an exadecimal color code: #FFFFFF for white")    
    danger = models.CharField(max_length=7, default="#FFFFFF", 
        help_text="Add an exadecimal color code: #FFFFFF for white")    
    success = models.CharField(max_length=7, default="#FFFFFF", 
        help_text="Add an exadecimal color code: #FFFFFF for white")    
    warning = models.CharField(max_length=7, default="#FFFFFF", 
        help_text="Add an exadecimal color code: #FFFFFF for white")   

    def __str__(self):
        return self.name                 

register_snippet(ColorPalette)

class FontStyle(models.Model):    
    """A color palette"""
    name = models.CharField(max_length=255, blank=True, null=True)
    font_color = models.ForeignKey(Color, related_name="font_color", null=True, on_delete=models.SET_NULL)    
    font_size = models.IntegerField(default=14, help_text="Font size in px")
    font_family = models.CharField(max_length=255, default="Montserrat", 
        help_text="Choose a Google font family")    
    font_style = models.CharField(max_length=7, default="bold")        
            
    def __str__(self):
        return self.name

register_snippet(FontStyle)

class Navbar(models.Model):    
    """A color palette"""
    name = models.CharField(max_length=255, blank=True, null=True)
    bg_color = models.ForeignKey('themes.Color', related_name="navbar_bg_color", on_delete=models.SET_NULL, null=True, blank=True)
    text_color = models.ForeignKey('themes.Color', related_name="navbar_text_color", on_delete=models.SET_NULL, null=True, blank=True)
    title_size = models.IntegerField(default=16, help_text="Font size in px")
    subtitle_size = models.IntegerField(default=11, help_text="Font size in px")
    subtitle_show = models.BooleanField(default=True)    
    
    def __str__(self):
        return self.name
   
register_snippet(Navbar)

class Footer(models.Model):    
    """Footer styling"""
    name = models.CharField(max_length=255, blank=True, null=True)
    bg_color = models.ForeignKey('themes.Color', related_name="footer_bg_color", on_delete=models.SET_NULL, null=True, blank=True)
    text_color = models.ForeignKey('themes.Color', related_name="footer_text_color", on_delete=models.SET_NULL, null=True, blank=True)
    title_size = models.IntegerField(default=16, help_text="Font size in px")
    subtitle_size = models.IntegerField(default=11, help_text="Font size in px")
    subtitle_show = models.BooleanField(default=True)    
    
    def __str__(self):
        return self.name

register_snippet(Footer)

class Jumbotron(models.Model):    
    """A color palette"""
    name = models.CharField(max_length=255, blank=True, null=True)
    bg_color = models.ForeignKey('themes.Color', related_name="jumbotron_bg_color", on_delete=models.SET_NULL, null=True, blank=True)
    text_color = models.ForeignKey('themes.Color', related_name="jumbotron_text_color", on_delete=models.SET_NULL, null=True, blank=True)
    title_size = models.IntegerField(default=16, help_text="Font size in px")
    button_color = models.ForeignKey('themes.ColorPalette', on_delete=models.SET_NULL, null=True, blank=True)
    button_size = models.IntegerField(default=14, help_text="Button size in rem")
    
    def __str__(self):
        return self.name

register_snippet(Jumbotron)

@register_setting
class Theme(BaseSetting):
    """Wrapper class to provide the other setting classes with some common methods"""
    
    color = models.ForeignKey("themes.ColorPalette", on_delete=models.SET_NULL, null=True, blank=True)
    font = models.ForeignKey("themes.FontStyle", on_delete=models.SET_NULL, null=True, blank=True)
    navbar = models.ForeignKey("themes.Navbar", on_delete=models.SET_NULL, null=True, blank=True)
    footer = models.ForeignKey("themes.Footer", on_delete=models.SET_NULL, null=True, blank=True)
    jumbotron = models.ForeignKey("themes.Jumbotron", on_delete=models.SET_NULL, null=True, blank=True)
   
    panels = [        
        FieldPanel('color'),
        FieldPanel('font'),
        FieldPanel('navbar'),
        FieldPanel('jumbotron'),
        FieldPanel('footer'),        
        ]

    class Meta:                
        verbose_name = "Theme Settings"

    ## A function that uses the values stored in the model to print to a file the corresponding Boostrap SCSS variables
    def print_scss(self):
        """Prints the SCSS variables contained in the model to a file, color, font and navbar"""
        with open("themes/theme.scss", "w") as f:

            f.write("$primary: #" + self.color.primary + ";\n")
            f.write("$secondary: #" + self.color.secondary + ";\n")
            f.write("$success: #" + self.color.success + ";\n")
            f.write("$info: #" + self.color.info + ";\n")
            f.write("$warning: #" + self.color.warning + ";\n")
            f.write("$danger: #" + self.color.danger + ";\n")
            f.write("$light: #" + self.color.light + ";\n")
            f.write("$dark: #" + self.color.dark + ";\n")


            f.write("$font-family: " + self.font.font_family + ";\n")
            f.write("$font-size: " + self.font.font_size + ";\n")
            f.write("$font-color: " + self.font.font_color + ";\n")
            f.write("$font-style: " + self.font.font_style + ";\n")
            f.write("$navbar-bg-color: " + self.navbar.bg_color + ";\n")
            f.write("$navbar-text-color: " + self.navbar.text_color + ";\n")
            f.write("$navbar-subtitle-size: " + self.navbar.subtitle_size + ";\n")
            f.write("$navbar-subtitle-show: " + self.navbar.subtitle_show + ";\n")
            f.write("$navbar-title-size: " + self.navbar.title_size + ";\n")
            f.write("$footer-bg-color: " + self.footer.bg_color + ";\n")
            f.write("$footer-text-color: " + self.footer.text_color + ";\n")
            f.write("$footer-subtitle-size: " + self.footer.subtitle_size + ";\n")
            f.write("$footer-subtitle-show: " + self.footer.subtitle_show + ";\n")
            f.write("$footer-title-size: " + self.footer.title_size + ";\n")
            f.write("$jumbotron-bg-color: " + self.jumbotron.bg_color + ";\n")
            f.write("$jumbotron-button-color: " + self.jumbotron.button_color + ";\n")
            f.write("$jumbotron-button-size: " + self.jumbotron.button_size + ";\n")            

        

    
    def compile_scss(self):
        """Compile the scss file and write the output to the css file"""

        NAME = settings.NAME

        # Compile the SCSS file into the CSS file
        compile_sass(
            inpath=os.path.join(NAME,'static/scss/', NAME, "theme.scss"),
            outpath=os.path.join(NAME, 'static/css/', NAME),
            output_style="compressed",
            precision=8,
            source_map=True
        )
        
        # If the file already exist, remove the previous file and replace it with the new one
        if os.path.exists(os.path.join('static/css/', NAME, 'theme.css')):
            # Remove the previous file
            os.remove(os.path.join('static/css/', NAME, 'theme.css'))
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
