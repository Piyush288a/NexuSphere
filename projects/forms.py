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


from .models import ProjectProposal

class ProjectProposalForm(forms.ModelForm):
    class Meta:
        model = ProjectProposal
        fields = ['title', 'description', 'proposed_project_lead', 'proposed_deadline']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter project title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Describe the project proposal',
                'rows': 6
            }),
            'proposed_project_lead': forms.Select(attrs={
                'class': 'form-select'
            }),
            'proposed_deadline': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Filter project leads to department members only
        if user and user.department:
            # Only show users from the same department with project_lead or collaboration role
            self.fields['proposed_project_lead'].queryset = User.objects.filter(
                department=user.department,
                role__in=['project_lead', 'collaboration']
            )
        
        # Update field labels
        self.fields['title'].label = 'Project Title'
        self.fields['description'].label = 'Project Description'
        self.fields['proposed_project_lead'].label = 'Proposed Project Lead'
        self.fields['proposed_deadline'].label = 'Proposed Deadline'


class TeamManagementForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_lead', 'members']
        widgets = {
            'project_lead': forms.Select(attrs={'class': 'form-select'}),
            'members': forms.SelectMultiple(attrs={
                'class': 'form-select-multiple',
                'size': '10',
            }),
        }

    def __init__(self, *args, **kwargs):
        department = kwargs.pop('department', None)
        super().__init__(*args, **kwargs)

        dept_users = User.objects.filter(department=department).order_by('username') if department else User.objects.none()

        self.fields['project_lead'].queryset = dept_users
        self.fields['project_lead'].label = 'Project Lead'
        self.fields['project_lead'].empty_label = '— Select project lead —'

        self.fields['members'].queryset = dept_users
        self.fields['members'].label = 'Team Members'
        self.fields['members'].required = False

    def clean(self):
        cleaned_data = super().clean()
        lead    = cleaned_data.get('project_lead')
        members = cleaned_data.get('members') or []

        if lead and members:
            # Ensure lead is also in members
            member_pks = [m.pk for m in members]
            if lead.pk not in member_pks:
                raise forms.ValidationError(
                    f"{lead.username} is the project lead and must also be listed as a team member."
                )

        return cleaned_data
