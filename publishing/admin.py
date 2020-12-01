from django.contrib import admin
from django.contrib.auth.models import Permission

class ApprovalAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Publishing', {
            'description': ('For the page to go live, the date/time must be reached AND "Approved to Publish" must be checked. Uncheck to pull a blog offline without deleting.'),
            'fields': ('content_review', 'visual_review', 'seo_review', 'approved'),
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        #Check permissions and disable checkboxes for users without permissions
        form = super().get_form(request, obj, **kwargs)
        user_can_review_content = request.user.has_perm('publishing.can_review_content')
        user_can_review_visual = request.user.has_perm('publishing.can_review_visual')
        user_can_review_seo = request.user.has_perm('publishing.can_review_seo')
        user_can_approve = request.user.has_perm('publishing.can_approve')

        if not user_can_review_content:
            form.base_fields['content_review'].disabled = True
        if not user_can_review_visual:
            form.base_fields['visual_review'].disabled = True
        if not user_can_review_seo:
            form.base_fields['seo_review'].disabled = True
        if not user_can_approve:
            form.base_fields['approved'].disabled = True

        return form

    def fieldsets(self):
        return self.fieldsets


#Allows you to create permissions in the admin for any model
@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('content_type')