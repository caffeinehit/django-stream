from django import template

register = template.Library()

@register.tag
def render_action(parser, token):
    """
    Renders a single action.
    """
    bits = token.split_contents()
    
    try:
        return ActionRenderNode(bits[1])
    except IndexError:
        raise template.TemplateSyntaxError('{% render_action %} takes exactly one argument.')
    
class ActionRenderNode(template.Node):
    def __init__(self, action):
        self.action = template.Variable(action)
    
    def render(self, context):
        action = self.action.resolve(context)
        
        try:
            return template.loader.render_to_string('stream/%s.html' % action.verb,
                {'action': action}, context)
        except template.TemplateDoesNotExist:
            return template.loader.render_to_string('stream/action.html',
                {'action': action}, context)
