from django.db import models

# Create your models here.
class Scan(models.Model):
    im =  models.ImageField(upload_to='images/')
 