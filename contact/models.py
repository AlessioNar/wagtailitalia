"""
from django.db import models

# Create your models here.
class FormField(AbstractFormField):
	
	page = ParentalKey('FormPage', on_delete=models.CASCADE,
		related_name='form_fields',

		)

class ContactPage(AbstractEmailForm):

	template = "contact/contact_page.html"
"""