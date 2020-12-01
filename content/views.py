from django.shortcuts import render
from .models import HomePage

# Create your views here.
def homePage(request):
    content = HomePage.object()

    template_name = 'content/home.html'
    context = {'content': content}

    return render(request, template_name, context)