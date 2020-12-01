from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.utils.html import strip_tags
from django.contrib.sitemaps import Sitemap
from django.utils import timezone
from meta_seo.models import MetaSEO
from publishing.models import ScheduledPublish, Approval

class Blog(MetaSEO, ScheduledPublish, Approval):
    image = models.ImageField(blank=True, upload_to='images/blogs/')
    
    """ author = models.ForeignKey(
        'author.Author', 
        on_delete = models.SET_NULL,
        null=True
    ) """
    
    subtitle = models.CharField(blank=True, max_length=300)

    body = models.TextField()
    
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    #Set up views for previewing vs. live. REQUIRED FIELDS (should match named views in views.py)
    live_view = 'blogPost'
    preview_view = 'blogPostPreview'

    def __str__(self):
        return self.title

    def excerpt(self):
        excerpt_no_html = strip_tags(self.body)
        return excerpt_no_html[:280]
    

    #If blog is being created, the URL will be auto-generated. After it's been saved, the URL is editable:
    #TODO: handle if slug is not unique
    def save(self, *args, **kwargs):
        if self.slug == '':
            value = self.title
            self.slug = slugify(kwargs.pop('slug', value)) #, allow_unicode=True)
            super(Blog, self).save(*args, **kwargs)
        else:
            super(Blog, self).save(*args, **kwargs)

        

    class Meta:
        unique_together = ('slug', 'publish_date')


class BlogSitemap(Sitemap):
    changefreq = "never"
    priority = 0.8
    def items(self):
        blogs = Blog.objects.filter(approved=True).filter(publish_date__lte=timezone.now()) 
        return blogs

    def lastmod(self, obj):
        return obj.date_updated