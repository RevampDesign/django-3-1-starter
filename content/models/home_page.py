from django.db import models
from single_page.models import SinglePage
from publishing.models import Approval
from django.urls import reverse

class HomePage(SinglePage, Approval):
    headline = models.CharField(max_length=300)

    fieldsets = (
        ('Meta / SEO', {
            'fields': ('title', 'description', 'keywords'),

        }),
        ('Page Content', {
            'fields': ('headline',),
        })
    )

    def get_absolute_url(self):
        return reverse('homePage')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural = "Home Page"