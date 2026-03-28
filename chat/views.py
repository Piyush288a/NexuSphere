from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Message
from projects.models import Project
from .forms import MessageForm


@login_required
def project_chat(request, project_id):
    """Display project chat and handle message sending"""
    project = get_object_or_404(Project, id=project_id)
    user = request.user

    # Check access permissions — return 403 for unauthorized (PART 12)
    has_access = False
    if user.role == 'admin':
        has_access = True
    elif user.role == 'dept_head' and user.department == project.department:
        has_access = True
    elif project.project_lead == user:
        has_access = True
    elif project.members.filter(pk=user.pk).exists():
        has_access = True

    if not has_access:
        return HttpResponseForbidden("You don't have permission to access this project's chat.")
    
    # Handle message submission
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.project = project
            message.sender = user
            message.save()
            messages.success(request, 'Message sent successfully!')
            return redirect('project_chat', project_id=project.id)
    else:
        form = MessageForm()
    
    # Get all messages for this project
    chat_messages = project.messages.all().order_by('created_at')
    
    context = {
        'project': project,
        'chat_messages': chat_messages,
        'form': form,
        'message_count': chat_messages.count(),
    }
    return render(request, 'chat/project_chat.html', context)
