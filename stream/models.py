from django import template
from django.db import models

from django.conf import settings
from django.utils.translation import ugettext as _

from stream.registry import model_map

DEFAULT_STREAM_CHOICES = (
    ('default', _('Stream Item')),
)

STREAM_CHOICES = getattr(settings, 'STREAM_CHOICES', DEFAULT_STREAM_CHOICES)

class StreamManager(models.Manager):
    
    def create(self, *objects, **kwargs):
        stream = super(StreamManager, self).create(**kwargs)
        for obj in objects:
            rel_name, f_name, m2m = model_map[obj.__class__]
            if m2m:
                field = getattr(stream, f_name)
                field.add(obj)
            else:
                setattr(stream, f_name, obj)
        stream.save()
        return stream

    def get_for_object(self, obj, **kwargs):
        rel_name, f_name, m2m = model_map[obj.__class__]
        kwargs.update({f_name:obj})
        return self.filter(**kwargs)


class Stream(models.Model):

    datetime = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length = 255, blank = False, null = False,
        default = STREAM_CHOICES[0][0])

    objects = StreamManager()

    def __unicode__(self):
        return u'Stream: %s %s' % (self.type, self.datetime)

    def render(self):
        tpl = template.loader.get_template('stream/%s.html' % self.type)
        return tpl.render(template.Context(dict(stream=self)))


