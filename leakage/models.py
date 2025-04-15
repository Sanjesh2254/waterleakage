from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class water_leakage(models.Model):
    flow1 = models.FloatField()
    flow2 = models.FloatField()
    flow3 = models.FloatField()
    pressure= models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.flow1) + " " + str(self.flow2) + " " + str(self.flow3) + " " + str(self.pressure) +" "+str(self.timestamp)
    

class Complaint(models.Model):
    zone = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    issue = models.TextField()
    coordinates = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def _str_(self):
        return f"{self.issue} at {self.location} by {self.user}"