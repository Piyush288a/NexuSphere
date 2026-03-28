from django.db.models import Q


def chat_sidebar(request):
    """
    Injects `chat_projects` into every template context.
    Only populated for authenticated collaboration users.
    Used by base.html to render the Slack-style chat channel sidebar.
    """
    if not request.user.is_authenticated or request.user.role != 'collaboration':
        return {'chat_projects': []}

    from projects.models import Project
    projects = (
        Project.objects
        .filter(Q(project_lead=request.user) | Q(members=request.user))
        .distinct()
        .only('id', 'project_name')
        .order_by('project_name')
    )
    return {'chat_projects': projects}
