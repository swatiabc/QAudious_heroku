from django.db import models
from transcribe_audio.models import AudioDataModel
from django.contrib.auth.models import User
# Create your models here.

class QADataModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    transcript = models.ForeignKey(AudioDataModel, on_delete=models.CASCADE)
    username = models.TextField(null=True,blank=True)
    question = models.TextField(null=True, blank=True)
    answer = models.TextField(null=True, blank=True)