from django.db import models

# Create your models here.
from django.db import models

class UserInfo(models.Model):
    age = models.IntegerField()
    genre = models.CharField(max_length=10)
    niveau_scolaire = models.CharField(max_length=100)
    ethnie = models.CharField(max_length=100)

class UserResponse(models.Model):
    user_info = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    question = models.TextField()
    response = models.CharField(max_length=10)
    vrairep = models.CharField(max_length=10, null=True, blank=True) 
    tempsmis = models.FloatField(null=True, blank=True) 
    timestamp = models.DateTimeField(auto_now_add=True)

