from django import forms 
from .models import TaskList
from django.core.exceptions import ValidationError


class ListForm(forms.ModelForm):

    class Meta:
        model = TaskList
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ListForm,self).__init__(*args, **kwargs)
        self.fields['task_type'].empty_label ="Task Type"

