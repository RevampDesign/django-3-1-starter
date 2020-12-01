from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User


""" Inherit classes according to needs for publishing. """

class Approval(models.Model):
    #Approval process that can be added to any page
    content_review = models.BooleanField(default=False)
    last_content_review_date = models.DateTimeField(auto_now=True)

    visual_review = models.BooleanField(default=False)
    last_visual_review_date = models.DateTimeField(auto_now=True)
    
    seo_review = models.BooleanField(default=False)
    last_seo_review_date = models.DateTimeField(auto_now=True)
    
    approved = models.BooleanField(default=False, help_text=('Final approval. Must be checked for this page to be live.'), verbose_name="Approved to Publish")
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    last_approval_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        permissions = [
            ("can_review_content", "Can Review Content"),
            ("can_review_visual", "Can Review Visuals"),
            ("can_review_seo", "Can Review SEO"),
            ("can_approve", "Can Approve to Publish"),
        ]


class ScheduledPublish(models.Model):
    #For being able to schedule pages to go live at specific times
    publish_date = models.DateTimeField()

    def publish_date_only(self):
        return self.publish_date.strftime('%e %B, %Y')

    #live_view, preview_view, and slug are REQUIRED when inheriting this class (used below)
    def get_absolute_url(self):
        """ For 'View on Site' buttons. Calls the View with the arguments needed to find the right page, in this case, the slug. If the page is approved and the publish date is reached, the 'View on Site' button will go to the live page, otherwise, it goes to the preview page. """
        kwargs = {
            'slug': self.slug
        }
        if self.approved and self.publish_date <= timezone.now():
            return reverse(self.live_view, kwargs=kwargs)
        else:
            return reverse(self.preview_view, kwargs=kwargs)

    class Meta:
        abstract = True
