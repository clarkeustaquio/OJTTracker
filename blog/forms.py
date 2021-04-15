from django import forms 
from .models import TaskList
from django.core.exceptions import ValidationError


class ListForm(forms.ModelForm):
    # start_time = forms.TimeField(widget=forms.TimeInput(attrs={'type':'time','placeholder':'Time'}))
    # end_time = forms.TimeField(widget=forms.TimeInput(attrs={'type':'time','placeholder':'Time'}))

    class Meta:
        model = TaskList
        fields = '__all__'
        # fields = [ 'start_time','end_time','task','task_type']
        # labels = {
      
        #     'task' :'What Task?',
           
        # }
        # widgets = {
             
              
        #     'task' : forms.TextInput(attrs={'placeholder':'What Task You did?' ,'style':'width:470px'}),
        #     'task_type':forms.Select(attrs={'style':'width:470px'}),
         
            
        # }
        

    def __init__(self, *args, **kwargs):
        super(ListForm,self).__init__(*args, **kwargs)
        self.fields['task_type'].empty_label ="Task Type"
