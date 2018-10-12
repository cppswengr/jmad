from django.shortcuts import render_to_response
from .models import Solo


def index(request):
    context = {'solos': Solo.objects.all()}
    return render_to_response('solos/index.html', context)
