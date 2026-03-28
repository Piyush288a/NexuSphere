from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def is_active_chat(context, project_id):
    """Returns True if the current request path is the chat page for this project."""
    request = context.get('request')
    if not request:
        return False
    return request.path == f'/projects/{project_id}/chat/'
