from django_sass import compile_sass, find_static_paths
import os
from django.core.management import call_command

from django.db import models

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
    css = models.TextField(
        blank=True, help_text="Add custom css", default='')

    panels = [
        MultiFieldPanel([
            FieldPanel("primary"),
            FieldPanel("secondary"),
            FieldPanel("light"),
            FieldPanel("dark"),
            FieldPanel("white"),
            FieldPanel("blue")
        ], heading="Color settings"),
        FieldPanel("css"),
    ]

    def save(self, *args, **kwargs):
        project_name = 'wagtailitalia'
        with open(project_name + '/static/scss/' + project_name + '/' + project_name + '.scss', 'w+') as f:
            # Define scss variables
            print(f'$primary: {self.primary} !default;', file=f)
            print(f'$secondary: {self.secondary} !default;', file=f)
            print(f'$dark: {self.dark} !default;', file=f)
            print(f'$light: {self.light} !default;', file=f)
            print(f'$white: {self.white} !default;', file=f)
            print(f'$blue: {self.blue} !default;', file=f)

            # Define imports
            print(
                "@import '" + project_name + "/static/scss/bootswatch/_variables.scss';", file=f)
            print(
                "@import '" + project_name + "/static/scss/bootstrap/bootstrap.scss';", file=f)
            print(
                "@import '" + project_name + "/static/scss/bootswatch/_bootswatch.scss';", file=f)

            # Add field for custom css
            print(self.css, file=f)

            # Compile scss and write to output file.
        compile_sass(
            inpath=project_name + '/static/scss/'
            + project_name + '/' + project_name + ".scss",
            outpath=project_name + '/static/css/'
            + project_name + '/' + project_name + ".css",
            output_style="compressed",
            precision=8,
            source_map=True
        )

        # Save in database
        super(ThemesSettings, self).save(*args, **kwargs)

        # checking whether file exists or not
        if os.path.exists(r'static/css/' + project_name + '/' + project_name + '.css'):
            # removing the main css file
            os.remove(r'static/css/' + project_name
                      + '/' + project_name + '.css')
        else:
            # file not found message
            print("CSS directory not found")

        # Call Collectstatic original method from manage.py
        call_command('collectstatic', '--no-input')
