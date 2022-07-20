"""Menus models."""
from django.db import models


from django_extensions.db.fields import AutoSlugField

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.admin.edit_handlers import (
	FieldPanel,
	MultiFieldPanel,
	InlinePanel,
	PageChooserPanel,

	)
from blog.models import BlogCategory

from wagtail.core.models import Orderable
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel


@register_snippet
class Menu(ClusterableModel):
	"""The main menu clusterable model"""

	title = models.CharField(max_length=100)
	slug = AutoSlugField(populate_from="title", editable=True)

	panels = [
		MultiFieldPanel([
			FieldPanel("title"),
			FieldPanel("slug"),
			], heading="Menu"),
		InlinePanel("menu_items", label="Menu Item")
	]

	def __str__(self):
		return self.title


class MenuItem(Orderable, ClusterableModel):
	"""The first level of the Menu"""

	link_title = models.CharField(blank=True, null=True, max_length=50)
	link_url = models.CharField(blank=True, null=True, max_length=500)

	link_page = models.ForeignKey(
		"wagtailcore.Page",
		null=True,
		blank=True,
		related_name="+",
		on_delete=models.SET_NULL
		)

	submenu = models.ForeignKey(
		"SubmenuItem",
		null=True,
		blank=True,
		related_name="+",
		on_delete=models.SET_NULL
		)

	open_in_new_tab = models.BooleanField(default=False, blank=True)

	# The connection to the main menu
	page = ParentalKey("Menu", related_name="menu_items")

	panels = [
            MultiFieldPanel([
		FieldPanel("link_title"),
		FieldPanel("link_url"),
		PageChooserPanel("link_page"),
                #	FieldPanel("tags"),
		FieldPanel("open_in_new_tab"),
                ], heading="Menu"),

            # The connection with the lower level of the menu
            InlinePanel("submenu_items", label="Submenu item")

	]

	@property
	def link(self):
		if self.link_page:
			return self.link_page.url
		elif self.link_url:
			return self.link_url
		return "#"

	@property
	def title(self):
		if self.link_page and not self.link_title:
			return self.link_page.title
		elif self.link_title:
			return self.link_title
		return 'Missing Title'

	@property
	def id(self):
		if self.link_page and not self.link_title:
			return self.link_page.title
		elif self.link_title:
			return self.link_title
		return 'Missing Title'


class SubmenuItem(Orderable):

	"""Subclassing menu items to create sublists"""
	link_title = models.CharField(blank=True, null=True, max_length=50)
	link_url = models.CharField(blank=True, null=True, max_length=500)
	open_in_new_tab = models.BooleanField(default=False, blank=True)

	link_page = models.ForeignKey(
		"wagtailcore.Page",
		null=True,
		blank=True,
		related_name="+",
		on_delete=models.SET_NULL
		)

	tags = models.ForeignKey(
		"blog.BlogTag",
		null=True,
		blank=True,
		related_name="+",
		on_delete=models.SET_NULL
		)

	menu_item = ParentalKey("MenuItem", related_name="submenu_items")

	panels = [
            MultiFieldPanel([
			FieldPanel("link_title"),
			MultiFieldPanel([
				
				FieldPanel("link_url"),
				PageChooserPanel("link_page"),
				FieldPanel("tags"),
				], heading="Urls"),
			FieldPanel("open_in_new_tab")
			], heading="Submenu Item"),
	]

	@property
	def link(self):
		if self.tags:
			tag_url = str(self.link_page.url) + '?tags=' + self.tags.slug
			return tag_url
		elif self.link_url:
			return self.link_url
		elif self.link_page:
			return self.link_page.url
		return "#"

	@property
	def title(self):
		if self.link_page and not self.link_title:
			return self.link_page.title
		elif self.link_title:
			return self.link_title
		return 'Missing Title'

	def __str__(self):
		return self.title
