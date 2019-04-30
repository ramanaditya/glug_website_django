from django.shortcuts import render
import io
import re
import os


# Create your views here.
def index(request):
    return render(request, 'events/index.html')
