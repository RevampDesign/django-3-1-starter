from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User


class MetaSEO(models.Model):
    #MetaSEO process that can be added to any page
    title = models.CharField(max_length=300)
    description = models.CharField(
        max_length=160,
        help_text=("Meta description; 160 characters max."),
        blank=True,
    )
    keywords = models.CharField(max_length=300, blank=True)

    slug = models.SlugField(blank=True, unique=True, max_length=300, help_text=("Auto-generated based on title. Full URL visible after saving..."))

    social_media_image = models.ImageField(blank=True, upload_to='images/social/')

    noindex_nofollow = models.BooleanField(default=False, help_text="Set the meta robots tag to noindex, nofollow")

    class Meta:
        abstract = True