#!/usr/bin/env python
import os
import sys
from google.cloud.bigquery.client import Client
from google.oauth2 import service_account
from django.conf import settings

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glug.settings')
    try:
        from django import db
        db.connections.close_all()
        
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
        

    #BASE_DIRS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    #dir_add = os.path.join(
    #    BASE_DIRS, "glug_website_django/glugmvit-web-firebase-adminsdk-fcfa3-d4143f72cc.json")
    #os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = settings.GOOGLE_APPLICATION_CREDENTIALS
    #bq_client = Client()

    
    execute_from_command_line(sys.argv)
