from django import forms
from events.models import *


class photo_form(forms.ModelForm):
    class Meta:
        model = Scan
        fields = ['im']