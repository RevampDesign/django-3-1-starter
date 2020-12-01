from django.forms import ModelForm
from tinymce.widgets import TinyMCE
from .models import Blog

class BlogAdminForm(ModelForm):
    class Meta:
        fields = '__all__'
        model = Blog
        widgets = {
            'body': TinyMCE(),
        }