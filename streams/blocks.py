"""Streamfields live in here"""

from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtailmarkdown.blocks import MarkdownBlock


class TitleBlock(blocks.StructBlock):
    """Title and text and nothing else."""
    background_color = blocks.BooleanBlock(
        required=False, help_text='Choose the background color: nothing for white, tick for grey')
    title = blocks.CharBlock(required=True, help_text='Add your title')

    class Meta:  # noqa
        template = "streams/title_block.html"
        icon = "edit"
        label = "Title"


class ImageBlock(blocks.StructBlock):
    """Simple Image insertion block"""

    caption = blocks.CharBlock(
        required=False, max_length=200, help_text="Add a caption")
    image = ImageChooserBlock(required=True)

    class Meta:  # noqa
        template = "streams/image_block.html"
        icon = "image"
        label = "Image"


class VerticalCardBlock(blocks.StructBlock):
    """Cards with image and text and button(s)"""

    title = blocks.CharBlock(required=True, help_text='Add your title')

#	source = models.ForeignKey("blog.BlogCategories")

    class Meta:  # noqa
        template = "streams/card_block.html"
        icon = "placeholder"
        label = "VerticalCardBlock"


class HorizontalCardBlock(blocks.StructBlock):
    """Cards with image and text and button(s)"""

    title = blocks.CharBlock(required=True, help_text='Add your title')
    text = blocks.RichTextBlock(required=False, help_text='Add your subtitle')
    image = ImageChooserBlock(
        required=True, help_text="Suggested image size: 300x200")
    button_text = blocks.CharBlock(
        required=True, help_text='Add the button text', default="Learn More")
    button_page = blocks.PageChooserBlock(required=False)
    button_url = blocks.URLBlock(
        required=False, help_text="If the button page above is selected, that will be used first")

    class Meta:  # noqa
        template = "streams/horizontal_card_block.html"
        icon = "placeholder"
        label = "Horizontal Card"


class RichtextBlock(blocks.RichTextBlock):
    """Richtext with all the features"""

    class Meta:  # noqa
        template = "streams/richtext_block.html"
        icon = "doc-full"
        label = "Full RichText"


class SimpleRichtextBlock(blocks.RichTextBlock):
    """Richtext without (limited) all the features"""

    def __init__(self, required=True, help_text=None, editor='default', features=None, **kwargs):
        super().__init__(**kwargs)
        self.features = [
            "bold",
            "italic",
            "link",
        ]

    class Meta:  # noqa
        template = "streams/richtext_block.html"
        icon = "edit"
        label = "Simple RichText"


class CTABlock(blocks.StructBlock):
    """Simple Call to Action section"""

    title = blocks.CharBlock(required=True, max_length=60)
    text = blocks.RichTextBlock(required=True, features=['bold', 'italic'])
    button_page = blocks.PageChooserBlock(required=False)
    button_url = blocks.URLBlock(required=False)
    button_text = blocks.CharBlock(
        required=True, default="Learn More", max_length=40)

    class Meta:  # noqa
        template = "streams/cta_block.html"
        icon = "placeholder"
        label = "Call to Action"


class LinkStructValue(blocks.StructValue):
    """Additional Logic for our urls"""

    def url(self):
        button_page = self.get('button_page')
        button_url = self.get('button_url')
        if button_page:
            return button_page.url
        elif button_url:
            return button_url

        return None

#	def latest_posts(self):
#		return BlogDetailPage.objects.live()[:3]


class ButtonBlock(blocks.StructBlock):
    """An external or internal URL"""

    button_page = blocks.PageChooserBlock(
        required=False, help_text="If selected, this url will be used first.")
    button_url = blocks.URLBlock(
        required=False, help_text="If added, this url will be used secondarily to the button page.")

#	def get_context(self, request, *args, **kwargs):
#		context = super().get_context(request, *args, **kwargs)
#		context['latest_posts'] = BlogDetailPage.objects.live().public()[:3]
#		return context

    class Meta:  # noqa
        template = "streams/button_block.html"
        icon = "placeholder"
        label = "Single Button"
        value_class = LinkStructValue


class BodyBlock(blocks.StructBlock):
    markdown = MarkdownBlock(required=False, icon="code",
                             help_text="Markdown syntax, easily convertible from latex. It supports document and image linking")

    class Meta:  # noqa
        template = "streams/markdown_block.html"
        icon = "placeholder"
        label = "Markdown"
