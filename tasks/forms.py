from django import forms
from .models import Task
from accounts.models import User

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'priority', 'deadline']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter task title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Enter task description',
                'rows': 4
            }),
            'assigned_to': forms.Select(attrs={
                'class': 'form-select'
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select'
            }),
            'deadline': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        project = kwargs.pop('project', None)
        super().__init__(*args, **kwargs)
        
        # Filter assigned_to to only show project members
        if project:
            self.fields['assigned_to'].queryset = project.members.all()
        
        # Update field labels
        self.fields['title'].label = 'Task Title'
        self.fields['description'].label = 'Description'
        self.fields['assigned_to'].label = 'Assign To'
        self.fields['priority'].label = 'Priority'
        self.fields['deadline'].label = 'Deadline'


class TaskStatusForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].label = 'Status'
