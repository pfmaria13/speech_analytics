from .models import Recordings
from django.forms import ModelForm

class RecordingForm(ModelForm):
    class Meta:
        model = Recordings
        fields = ['speed', 'text']

        widgets = {

        }