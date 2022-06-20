from django.db import models
from django_extensions.db.fields import AutoSlugField
from wagtail.admin.edit_handlers import FieldPanel

from wagtail.snippets.models import register_snippet


# Create your models here.
class Website(models.Model):
    """Website for a snippet"""
    name = models.CharField(max_length=255)
    url = models.URLField(blank=True, null=True)
    slug = AutoSlugField(
        populate_from=["name"],
        editable=True,
        help_text='A slug to identify websites',
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
        FieldPanel("url"),
	]

    class Meta:
        verbose_name="Website"
        verbose_name_plural="Websites"
        ordering=["name"]

    def __str__(self):
        """String Wrapper of this class"""
        return self.name

register_snippet(Website)
