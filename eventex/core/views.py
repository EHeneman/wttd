from django.shortcuts import render
from django.conf import settings


def home(request):
    context = {'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY}
    return render(request, 'index.html', context)
