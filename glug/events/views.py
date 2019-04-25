from django.shortcuts import render
import argparse
import io
import re
import os
from events.forms import *


# Create your views here.
def index(request):
    return render(request, 'events/index.html')

def Scan(request):
    
    if request.method == 'POST':
        im_form = photo_form(request.POST, request.FILES)
        if im_form.is_valid():
            im_form.save()
            #extracting the file name of the image being uploaded
            for filename, file in request.FILES.items():
                f_name = request.FILES[filename].name

            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            path =  os.path.join(BASE_DIR, 'media/images/'+f_name)
            #path = os.path.join(path,f_name)
            
            
                
            """Detects text in the file."""
            from google.cloud import vision
            client = vision.ImageAnnotatorClient()

            # [START vision_python_migration_text_detection]
            with io.open(path, 'rb') as image_file:
                content = image_file.read()

            image = vision.types.Image(content=content)

            response = client.text_detection(image=image)
            texts = response.text_annotations
            print('Texts:')
            s = []
            for text in texts:
                s.append(text.description)

            return render(request,'events/verify.html',{'im_form':s})
                
    
    else:
        im_form = photo_form()
    return render(request,'events/result.html',{'im_form':im_form})
