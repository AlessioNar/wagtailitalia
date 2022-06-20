from django.db import models

class Subscriber(models.Model):
	"""A subscriber model"""
	email = models.CharField(max_length=100, blank=False, null=False, help_text="Email Address")
	full_name = models.CharField(max_length=100, blank=False, null=False, help_text="Full Name")
	
	def __str__(self):
		"""Str representation of this object"""
		return self.full_name
