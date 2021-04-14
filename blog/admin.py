from django.contrib import admin
from .models import Destination, TaskList, TaskType

admin.site.register(Destination)
admin.site.register(TaskList)
admin.site.register(TaskType)