#!/usr/bin/env python
import os
import sys
from google.cloud.bigquery.client import Client

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'glug.settings')
    try:
        
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
        
    BASE_DIRS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dir_add = os.path.join(BASE_DIRS,"glug/glug-mvit1-firebase-adminsdk-e5ljh-474945bd09.json")
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = dir_add
    bq_client = Client()
    
    execute_from_command_line(sys.argv)
