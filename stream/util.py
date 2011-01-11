from stream.models import Stream
from stream.registry import registry, model_map
from django.db.models.fields.related import ManyToManyField, ForeignKey

def add(*objects, **kwargs):
    return Stream.objects.create(*objects, **kwargs)

def register(model, field_name = None, m2m = False):
    """
    Sets the given model class and stream classes up to working together
    """
    if model in registry:
        return

    registry.append(model)

    related_name = 'stream_%s' % model._meta.module_name

    if not field_name:
        field_name = model._meta.module_name

    # Create foreignkeys by default - less sql queries for lookups
    if m2m:
        field = ManyToManyField(
            model,
            related_name = related_name
            )
    else:
        field = ForeignKey(
            model,
            related_name = related_name,
            blank = True,
            null = True
        )
    field.contribute_to_class(Stream, field_name)

    # We need to keep track of which fields and which kind of fields point where
    model_map[model] = [related_name, field_name, m2m]
