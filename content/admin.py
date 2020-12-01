from django.contrib import admin

from .models import HomePage
from single_page.admin import SinglePageModelAdmin


class HomePageAdmin(SinglePageModelAdmin):
    list_display = ('__str__', 'content_review', 'visual_review', 'seo_review', 'approved')
    list_filter = ('content_review', 'visual_review', 'seo_review', 'approved')
    search_fields = ('title', 'body')

    #Organize the Admin Page. Removed slug field since it's the home page. (Be sure to include the inherited fields)
    fieldsets = (
        ('Meta / SEO', {
            'fields': ('title', 'description', 'keywords',)
        }),
        ('Content', {
            'fields': ('headline', ),
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


admin.site.register(HomePage, HomePageAdmin)