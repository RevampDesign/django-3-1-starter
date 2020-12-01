from django.contrib import admin
from django.conf.urls import url
from django.utils.html import format_html
from django.urls import reverse, path

# from .forms import BlogAdminForm
from .models import Blog

from publishing.admin import ApprovalAdmin

class BlogAdmin(ApprovalAdmin):
    list_display = ('__str__', 'publish_date', 'content_review', 'visual_review', 'seo_review', 'approved')
    list_filter = ('date_created', 'publish_date', 'content_review', 'visual_review', 'seo_review', 'approved')
    date_hierarchy = 'publish_date'
    search_fields = ('title', 'slug', 'body')

    #Organize the Blog Admin Create/Edit Page (Be sure to include the inherited approval fields)
    fieldsets = (
        ('Meta / SEO', {
            'fields': ('title', 'description', 'keywords', 'slug')
        }),
        ('Media / Podcast Options', {
            'fields': ('image',),
        }),
        ('Content', {
            'fields': ('subtitle', 'body'),
        }),
        ('Publishing', {
            'description': ('For the blog to go live, the date/time must be reached AND "Approved to Publish" must be checked. Uncheck to pull a blog offline without deleting.'),
            'fields': ('publish_date', 'content_review', 'visual_review', 'seo_review', 'approved'),
        }),
    )

    # form = BlogAdminForm

    #Make slug editable after saving the new blog
    def get_readonly_fields(self, request, obj=None):
        if obj is None: # saving a new object
            return ['slug']
        else: # editing an existing object
            return []


admin.site.register(Blog, BlogAdmin)