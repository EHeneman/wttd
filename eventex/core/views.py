from django.shortcuts import render
from eventex.settings import GOOGLE_MAPS_API_KEY


def home(request):
    context = {'GOOGLE_MAPS_API_KEY': GOOGLE_MAPS_API_KEY}
    return render(request, 'index.html', context)
