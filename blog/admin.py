from django.contrib import admin
from .models import Destination, TaskList, TaskType, Section

admin.site.register(Destination)
admin.site.register(TaskList)
admin.site.register(TaskType)
admin.site.register(Section)