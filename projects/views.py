from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseForbidden
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .models import Project, ProjectProposal
from .forms import ProjectProposalForm, TeamManagementForm


@login_required
def projects_list(request):
    """Display projects accessible to the logged-in user."""
    user = request.user

    if user.role == 'admin':
        projects = Project.objects.all()
    elif user.role == 'dept_head':
        projects = Project.objects.filter(department=user.department) if user.department else Project.objects.none()
    elif user.role == 'project_lead':
        projects = Project.objects.filter(project_lead=user)
    else:
        # collaboration — redirect to the filtered my-projects view
        return redirect('my_projects')

    projects = projects.select_related('department', 'project_lead').order_by('-created_at')
    for project in projects:
        project.members_count = project.members.count()

    return render(request, 'projects/list.html', {'projects': projects})


@login_required
def my_projects(request):
    """
    Collaboration-only view: projects where the user is lead OR a member.
    Backend-enforced — no other projects leak through.
    """
    user = request.user

    projects = Project.objects.filter(
        Q(project_lead=user) | Q(members=user)
    ).distinct().select_related('department', 'project_lead').order_by('-created_at')

    for project in projects:
        project.members_count = project.members.count()

    return render(request, 'projects/my_projects.html', {'projects': projects})


@login_required
def project_detail(request, project_id):
    """Display project details with strict per-role access control."""
    project = get_object_or_404(Project, id=project_id)
    user = request.user

    # --- Access control ---
    if user.role == 'admin':
        pass  # full access
    elif user.role == 'dept_head':
        if user.department != project.department:
            return HttpResponseForbidden("You don't have access to this project.")
    elif user.role == 'project_lead':
        if project.project_lead != user:
            return HttpResponseForbidden("You don't have access to this project.")
    else:
        # collaboration: must be an explicit member
        if not project.members.filter(pk=user.pk).exists():
            return HttpResponseForbidden("You are not a member of this project.")

    members = project.members.all().order_by('username')
    tasks   = project.tasks.all().order_by('-created_at')

    context = {
        'project': project,
        'members': members,
        'tasks': tasks,
        'members_count': members.count(),
        'tasks_count': tasks.count(),
    }
    return render(request, 'projects/detail.html', context)


@login_required
def manage_team(request, project_id):
    """
    PARTS 2, 8, 10 — Team management page.
    Only the Department Head of the project's department may access this.
    """
    project = get_object_or_404(Project, id=project_id)
    user    = request.user

    # PART 8 & 10 — strict access control
    if user.role != 'dept_head':
        return HttpResponseForbidden("Only the Department Head of this project's department can manage the team.")
    if user.department != project.department:
        return HttpResponseForbidden("You can only manage teams for projects in your own department.")

    if request.method == 'POST':
        form = TeamManagementForm(request.POST, instance=project, department=project.department)
        if form.is_valid():
            project = form.save(commit=False)
            project.save()

            # PART 6 — ensure project_lead is always in members
            members = list(form.cleaned_data['members'])
            lead    = form.cleaned_data['project_lead']
            if lead and lead not in members:
                members.append(lead)
            project.members.set(members)

            messages.success(request, f'Team updated for "{project.project_name}".')
            return redirect('project_detail', project_id=project.id)
    else:
        form = TeamManagementForm(instance=project, department=project.department)

    context = {
        'project': project,
        'form': form,
        'dept_users': project.department.users.order_by('username'),
    }
    return render(request, 'projects/manage_team.html', context)


@login_required
def proposal_create(request):
    """
    Create a new project proposal
    Only Department Heads can create proposals
    """
    user = request.user
    
    # Only dept_head can create proposals
    if user.role != 'dept_head':
        messages.error(request, "Only Department Heads can create project proposals.")
        return redirect('projects_list')
    
    if not user.department:
        messages.error(request, "You must be assigned to a department to create proposals.")
        return redirect('projects_list')
    
    if request.method == 'POST':
        form = ProjectProposalForm(request.POST, user=user)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.department = user.department
            proposal.proposed_by = user
            proposal.status = 'Pending'
            proposal.save()
            messages.success(request, f'Project proposal "{proposal.title}" submitted successfully!')
            return redirect('proposal_list')
    else:
        form = ProjectProposalForm(user=user)
    
    context = {
        'form': form,
    }
    return render(request, 'projects/proposal_create.html', context)


@login_required
def proposal_list(request):
    """
    List project proposals
    - Admin: sees all proposals
    - Dept Head: sees only their department's proposals
    """
    user = request.user
    
    if user.role == 'admin':
        proposals = ProjectProposal.objects.all()
    elif user.role == 'dept_head' and user.department:
        proposals = ProjectProposal.objects.filter(department=user.department)
    else:
        messages.error(request, "You don't have permission to view proposals.")
        return redirect('projects_list')
    
    proposals = proposals.order_by('-created_at')
    
    context = {
        'proposals': proposals,
    }
    return render(request, 'projects/proposal_list.html', context)


@login_required
def proposal_detail(request, proposal_id):
    """View proposal details"""
    proposal = get_object_or_404(ProjectProposal, id=proposal_id)
    user = request.user
    
    # Access control
    has_access = False
    if user.role == 'admin':
        has_access = True
    elif user.role == 'dept_head' and user.department == proposal.department:
        has_access = True
    
    if not has_access:
        raise Http404("You don't have permission to view this proposal.")
    
    context = {
        'proposal': proposal,
        'can_approve': user.role == 'admin' and proposal.status == 'Pending',
    }
    return render(request, 'projects/proposal_detail.html', context)


@login_required
def proposal_approve(request, proposal_id):
    """
    Approve a project proposal and create the actual project
    Admin only
    """
    user = request.user
    
    if user.role != 'admin':
        messages.error(request, "Only admins can approve proposals.")
        return redirect('proposal_list')
    
    proposal = get_object_or_404(ProjectProposal, id=proposal_id)
    
    if proposal.status != 'Pending':
        messages.error(request, "This proposal has already been processed.")
        return redirect('proposal_detail', proposal_id=proposal.id)
    
    if request.method == 'POST':
        # Create the actual project
        project = Project.objects.create(
            project_name=proposal.title,
            description=proposal.description,
            department=proposal.department,
            project_lead=proposal.proposed_project_lead,
            deadline=proposal.proposed_deadline,
        )
        
        # Update proposal status
        proposal.status = 'Approved'
        proposal.approved_at = timezone.now()
        proposal.created_project = project
        proposal.admin_notes = request.POST.get('admin_notes', '')
        proposal.save()
        
        messages.success(request, f'Proposal approved! Project "{project.project_name}" has been created.')
        return redirect('project_detail', project_id=project.id)
    
    context = {
        'proposal': proposal,
    }
    return render(request, 'projects/proposal_approve.html', context)


@login_required
def proposal_reject(request, proposal_id):
    """
    Reject a project proposal
    Admin only
    """
    user = request.user
    
    if user.role != 'admin':
        messages.error(request, "Only admins can reject proposals.")
        return redirect('proposal_list')
    
    proposal = get_object_or_404(ProjectProposal, id=proposal_id)
    
    if proposal.status != 'Pending':
        messages.error(request, "This proposal has already been processed.")
        return redirect('proposal_detail', proposal_id=proposal.id)
    
    if request.method == 'POST':
        proposal.status = 'Rejected'
        proposal.rejected_at = timezone.now()
        proposal.admin_notes = request.POST.get('admin_notes', '')
        proposal.save()
        
        messages.success(request, f'Proposal "{proposal.title}" has been rejected.')
        return redirect('proposal_list')
    
    context = {
        'proposal': proposal,
    }
    return render(request, 'projects/proposal_reject.html', context)
