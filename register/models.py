from django.db import models
from transcribe_audio.models import AudioDataModel

# Create your models here.
class Dashboard(models.Model):
    transcript = models.ForeignKey(AudioDataModel, on_delete=models.CASCADE)
    f_name = models.TextField(null=True, blank=True)
    l_name = models.TextField(null=True, blank=True)
    u_name = models.TextField(null=True, blank=True)
    email = models.EmailField(max_length = 254) 
    password1 = models.CharField(max_length=100)
    password2 = models.CharField(max_length=100)