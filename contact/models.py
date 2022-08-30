from django.db import models
from modelcluster.fields import ParentalKey

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel, StreamFieldPanel
from wagtail.core.fields import RichTextField, StreamField
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField

from wagtail.core.models import Page

from streams import blocks


class FormField(AbstractFormField):
	
	page = ParentalKey('ContactPage',
		on_delete=models.CASCADE,
		related_name='form_fields',
		)

class ContactPage(AbstractEmailForm, Page):

	template = 'contact/contact_page.html'

	intro = RichTextField(blank=True)
	thank_you_text = RichTextField(blank=True)

	heading_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.SET_NULL,
        help_text="Image used as a banner, suggested 1200 × 400 px",

    )

	content = StreamField(
        [
            ("title", blocks.TitleBlock()),
            ("richtext", blocks.RichtextBlock()),
            ("vertical_card", blocks.VerticalCardBlock()),
            ("horizontal_card", blocks.HorizontalCardBlock()),
            ("multiple_vertical_card_block", blocks.MultipleVerticalCardBlocks()),
            ("multiple_buttons_block", blocks.CardMultipleButtonBlock()),
            ("free_card", blocks.FreeVerticalCardsBlock()),
            ("cta", blocks.CTABlock()),
            ("image", blocks.ImageBlock()),
            ("markdown", blocks.BodyBlock()),
            ("video", blocks.VideoBlock()),

        ],
        null=True,
        blank=True
    )

	content_panels = AbstractEmailForm.content_panels + [
					FieldPanel('intro'),
					InlinePanel('form_fields', label="Form fields"),
					FieldPanel('thank_you_text'),
					MultiFieldPanel([
						FieldRowPanel([
							FieldPanel('from_address', classname="col6"),
							FieldPanel('to_address', classname="col6"),
						]),
						FieldPanel('subject'),
					], "Email settings"),
					FieldPanel('heading_image'),
					StreamFieldPanel("content"),
					
				]
	