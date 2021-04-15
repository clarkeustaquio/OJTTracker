from django.db import models
from datetime import time,date,datetime
from accounts.models import CustomUser

class Destination(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='pics')
    desc = models.TextField()
    price = models.IntegerField()
    offer = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class TaskType(models.Model):
    title = models.CharField(max_length=50)
    def __str__(self):
        return self.title
    
    
class TaskList(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    start_time = models.TimeField(auto_now=False, auto_now_add=False, null=True)
    end_time = models.TimeField(auto_now=False, auto_now_add=False, null=True)
    task = models.CharField(max_length=100)
    task_type = models.CharField(max_length=20)

    is_send = models.BooleanField(default=False)
    is_employee_accepted = models.BooleanField(default=False)

    def __str__(self):
        return self.task

