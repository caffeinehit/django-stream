from django.db.models.fields.related import ForeignKey

from stream.models import Action
from stream.registry import actor_registry, actor_map, target_registry, \
    target_map, action_object_registry, action_object_map


def _register(model, field_name, related_name, model_registry, model_map):
    """ Set up the foreign keys on the `Action` model """
    if model in model_registry:
        return
    
    model_registry.append(model)
    
    field = ForeignKey(model, related_name=related_name, blank=True, null=True,
        db_index=True)
    field.contribute_to_class(Action, field_name)
    
    model_map[model] = [related_name, field_name]

def __register(_field_name, _related_name, _registry, _model_map):
    def wrap(model, field_name=None, related_name=None):
        """ 
        Register a model with the stream application. 
        """
        
        if isinstance(model, list):
            for m in model:
                wrapper = __register(_field_name, _related_name, _registry, _model_map)
                wrapper(m, field_name, related_name)
        else:
            if field_name is None:
                field_name = _field_name % model._meta.module_name
            if related_name is None:
                related_name = _related_name % model._meta.module_name
                
            _register(model, field_name, related_name, _registry, _model_map)

    return wrap

register_actor = __register('actor_%s', 'actions_%s', actor_registry, actor_map)
register_target = __register('target_%s', 'targetted_%s', target_registry, target_map)
register_action_object = __register('action_%s', 'acted_%s', action_object_registry,
    action_object_map)



class action(object):
    @classmethod
    def send(cls, actor, verb, target=None, action_object=None, description=None):
        """
        Create an action
        """
        return Action.objects.create(actor, verb, target, action_object,
            description=description)
    

