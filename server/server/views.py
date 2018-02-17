from __future__ import unicode_literals
from django.template.response import TemplateResponse

def index_view(request):
    context = {}
    return TemplateResponse(request, 'index.html', context)


