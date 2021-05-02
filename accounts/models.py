from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    is_student = models.BooleanField(default=False)
    previous_day = models.DateField(null=True, blank=True)
    day_login = models.DateField(null=True, blank=True)
    is_switch = models.BooleanField(default=False)
    is_send = models.BooleanField(default=False)

    is_employee = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    teacher_students = models.ManyToManyField("self", blank=True)
    employee_students = models.ManyToManyField("self", blank=True)

    my_teacher = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE, related_name="student_teacher")
    my_employee = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE, related_name="student_employee")

    
    pending_employee = models.BooleanField(default=False)

    # Teacher & Employee
    is_male = models.BooleanField(default=False)
    phone = models.CharField(max_length=20, null=True, blank=True)
    question = models.CharField(max_length=50, null=True, blank=True)
    answer = models.CharField(max_length=250, null=True, blank=True)

    # Student - Employee
    is_student_approve = models.BooleanField(default=False)
    employer_student = models.ManyToManyField("self", blank=True)

    # Teacher - Student
    pending_teacher = models.BooleanField(default=False)
    accept_teacher = models.BooleanField(default=False)
    


