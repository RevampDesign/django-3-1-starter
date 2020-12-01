from __future__ import absolute_import, print_function, unicode_literals
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.db import models

from functools import wraps

from django.utils.encoding import force_text
from django.http import HttpResponseRedirect

#Page model credit: https://github.com/ionata/django-singletons

def page_view(fn_name):
    def view(self, request, object_id, extra_context=None):
        object_id = '1'
        self.model.objects.get_or_create(pk=1)

        super_view = getattr(super(SinglePageModelAdmin, self), fn_name)
        return super_view(request, object_id, extra_context=extra_context)

    view.__name__ = str(fn_name)
    return view


class SinglePageModelAdmin(admin.ModelAdmin):

    change_form_template = "admin/change_form.html"
    object_history_template = "admin/object_history.html"

    #Make slug editable after saving the new page
    def get_readonly_fields(self, request, obj=None):
        if obj is None: # saving a new object
            return ['slug']
        else: # editing an existing object
            return []

    #Get dynamic fieldsets
    def get_fieldsets(self, request, obj=None):
        self.fieldsets = obj.fieldsets
        return super(SinglePageModelAdmin, self).get_fieldsets(request, obj)

    def has_add_permission(self, request):
        """ Page pattern: prevent addition of new objects """
        return False

    def has_delete_permission(self, request, obj=None):
        """ Page pattern: prevent deletion of THE object """
        return False

    def get_urls(self):
        from django.conf.urls import url

        def wrap(view):
            @wraps(view)
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return wrapper

        info = self.model._meta.app_label, self.model._meta.model_name

        urlpatterns = [
            url(r'^history/$',
                wrap(self.history_view),
                {'object_id': 1},
                name='%s_%s_history' % info),
            url(r'^$',
                wrap(self.change_view),
                {'object_id': 1},
                name='%s_%s_change' % info),
            url(r'^$',
                wrap(self.changelist_view),
                name='%s_%s_changelist' % info),
        ]

        return urlpatterns

    def response_change(self, request, obj):
        #Determines the HttpResponse for the change_view stage.
        opts = obj._meta

        msg = _('%(obj)s was changed successfully.') % {'obj': force_text(obj)}
        if "_continue" in request.POST:
            self.message_user(request, msg + ' ' + _("You may edit it again below."))
            return HttpResponseRedirect(request.path)
        else:
            self.message_user(request, msg)
            return HttpResponseRedirect("../")

    change_view = page_view('change_view')

    history_view = page_view('history_view')