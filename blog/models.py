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
    date_created = models.DateField(auto_now_add=True)

    is_send = models.BooleanField(default=False)
    is_employee_accepted = models.BooleanField(default=False)
    finish_report = models.BooleanField(default=False)

    is_current = models.BooleanField(default=False)

    def __str__(self):
        return self.task

class Section(models.Model):
    section_name = models.CharField(max_length=150)
    section_code = models.CharField(max_length=50, unique=True)
    students = models.ManyToManyField(CustomUser, blank=True)
    school_name = models.CharField(max_length=150, default='New Era')

    def __str__(self):
        return self.section_name

    def update_code(self):
        section_id = self.id
        generate_code = 'SC' + "{0:03}".format(section_id)
        Section.objects.filter(id=section_id).update(section_code=generate_code)

    def save(self, *args, **kwargs):
        super(Section, self).save(*args, **kwargs)
        self.update_code()