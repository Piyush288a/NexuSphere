from django import forms
from .models import Project
from departments.models import Department
from accounts.models import User

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_name', 'description', 'department', 'project_lead', 'members', 'deadline']
        widgets = {
            'project_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter project name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Enter project description',
                'rows': 4
            }),
            'department': forms.Select(attrs={
                'class': 'form-select'
            }),
            'project_lead': forms.Select(attrs={
                'class': 'form-select'
            }),
            'members': forms.SelectMultiple(attrs={
                'class': 'form-select-multiple'
            }),
            'deadline': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Filter departments based on user role
        if user:
            if user.role == 'admin':
                self.fields['department'].queryset = Department.objects.all()
            elif user.role == 'dept_head' and user.department:
                self.fields['department'].queryset = Department.objects.filter(id=user.department.id)
                self.fields['department'].initial = user.department
            elif user.role == 'project_lead' and user.department:
                self.fields['department'].queryset = Department.objects.filter(id=user.department.id)
                self.fields['department'].initial = user.department
        
        # Update field labels
        self.fields['project_name'].label = 'Project Name'
        self.fields['description'].label = 'Description'
        self.fields['department'].label = 'Department'
        self.fields['project_lead'].label = 'Project Lead'
        self.fields['members'].label = 'Team Members'
        self.fields['deadline'].label = 'Deadline'
        
        # Make members optional initially
        self.fields['members'].required = False
    
    def clean(self):
        cleaned_data = super().clean()
        department = cleaned_data.get('department')
        project_lead = cleaned_data.get('project_lead')
        members = cleaned_data.get('members')
        
        # Validate project lead belongs to department
        if project_lead and department:
            if project_lead.department != department:
                raise forms.ValidationError(
                    f"Project lead must belong to the {department.department_name} department."
                )
        
        # Validate all members belong to the same department
        if members and department:
            for member in members:
                if member.department != department:
                    raise forms.ValidationError(
                        f"All team members must belong to the {department.department_name} department. "
                        f"{member.username} belongs to a different department."
                    )
        
        return cleaned_data
