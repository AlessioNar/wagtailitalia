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


	brand_name = models.CharField(blank=False, null=True, help_text="Brand Name", max_length=250)
	brand_image = models.ForeignKey(
		"wagtailimages.Image",
		on_delete=models.SET_NULL,
		null=True,
		blank=False,
		related_name ="+",
		)
	brand_subtitle = models.CharField(blank=True, null=True, help_text="A subtitle, optional", max_length=300)

	brand_website = models.URLField(blank=False, null=False, help_text="Brand URL")

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
		related_name ="+",
		)
	panels = [
		ImageChooserPanel('funding_image'),
	]