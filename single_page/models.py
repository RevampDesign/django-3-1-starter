from django.db import models
from django.utils.translation import gettext_lazy as _
from meta_seo.models import MetaSEO
from django.template.defaultfilters import slugify

# All single / one-off pages inherit SinglePage class which contains all the meta data. Child class contains all the content

class SinglePage(MetaSEO):

    class Meta:
        abstract = True

    #If page is being created, the URL will be auto-generated. After it's been saved, the URL is editable:
    #TODO: handle if slug is not unique
    #Only ever one instance of this page
    def save(self, *args, **kwargs):
        self.id=1

        if self.slug == '':
            value = self.title
            self.slug = slugify(kwargs.pop('slug', value))
            super(SinglePage, self).save(*args, **kwargs)
        else:
            super(SinglePage, self).save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        pass

    # How to get the only object from this model:
    @classmethod
    def object(cls):
        return cls._default_manager.all().first()