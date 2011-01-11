# Stream

Provides activity streams for Django models.

## Installation

    pip install django-stream

## Configuration

In your `settings.py` add stream types:

    INSTALLED_APPS += ('stream', )
    
    STREAM_CHOICES = (
        ('default', 'Stream Item'),
        ('edit', 'Object edited'),
        ('created','Object created'),
        ('deleted','Object deleted'),
    )

Make sure `stream` is added to `INSTALLED_APPS` after all the apps you intend
to use it on.

## Usage

To enable streams on models, register them in your `models.py`:

    from stream import add, register
    register(MyModel)
    register(MyOtherModel, m2m=True)

Running `syncdb` will then create the db table.

To add stream updates:

    obj = MyModel.objects.get(pk=1)
    add(obj, type='default')
    
    other_obj = MyModel.objects.get(pk=100)
    add(other_obj, type='edit')

    third_obj = MyModel.objects.create()
    add(third_obj, type='created')

To get the streams items:

    from stream.models import Stream
    Stream.objects.get_for_object(third_obj)


