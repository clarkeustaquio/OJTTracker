from django.db import models
from datetime import time,date,datetime

class Destination(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='pics')
    desc = models.TextField()
    price = models.IntegerField()
    offer = models.BooleanField(default=False)
    
class Task_type(models.Model):
    title = models.CharField(max_length=50)
    def __str__(self):
        return self.title
    
    
class List(models.Model):
    start_time = models.TimeField(auto_now=False, auto_now_add=False, null=True)
    end_time = models.TimeField(auto_now=False, auto_now_add=False, null=True)
    task = models.CharField(max_length=100)
    task_type = models.ForeignKey(Task_type, on_delete=models.CASCADE)


