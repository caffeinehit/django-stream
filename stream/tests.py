from django import template
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.test import TestCase
from stream import signals
from stream.models import Action
from stream import utils


utils.register_actor([User, Group])
utils.register_target([User, Group])
utils.register_action_object([User, Group])


class TestStream(TestCase):
    def setUp(self):
        self.lennon = User.objects.create(username='lennon')
        self.hendrix = User.objects.create(username='hendrix')
        self.morrison = User.objects.create(username='morrison')
        
    def test_create(self):
        obj1 = Action.objects.create(self.lennon, 'follow', self.hendrix)
        
        obj2, created = Action.objects.get_or_create(self.lennon, 'follow', self.hendrix)
        self.assertEqual(False, created) 
    
        self.assertEqual(obj1, obj2)
        
        obj1 = utils.action.send(self.lennon, 'follow', self.morrison)
        obj2, created = Action.objects.get_or_create(self.lennon, 'follow', self.morrison)
        
        self.assertEqual(obj1, obj2)
    
    def test_get_or_create(self):
        obj, created = Action.objects.get_or_create(self.lennon, 'follow', self.hendrix)
        self.assertEqual(True, created)

    def test_get_for_actor(self):
        Action.objects.create(self.lennon, 'follow', self.morrison)
        Action.objects.create(self.lennon, 'follow', self.hendrix)
        
        actions = Action.objects.get_for_actor(self.lennon)
        
        self.assertEqual(2, len(actions))

    def test_get_for_target(self):
        Action.objects.create(self.lennon, 'follow', self.morrison)
        Action.objects.create(self.hendrix, 'follow', self.morrison)
        
        actions = Action.objects.get_for_target(self.morrison)
        
        self.assertEqual(2, len(actions))
    
    def test_get_for_action_object(self):
        Action.objects.create(self.lennon, 'follow', self.morrison, self.hendrix)
        Action.objects.create(self.morrison, 'follow', self.lennon, self.hendrix)
        
        actions = Action.objects.get_for_action_object(self.hendrix)
        
        self.assertEqual(2, len(actions))

    def test_getters_setters(self):
        action = Action.objects.create(self.lennon, 'follow', self.morrison, self.hendrix)
        
        self.assertEqual(self.lennon, action.actor)
        self.assertEqual(self.morrison, action.target)
        self.assertEqual(self.hendrix, action.action_object)
    
        action.actor = self.morrison
        action.target = self.hendrix
        action.action_object = self.lennon
        action.save()
        
        action = Action.objects.get(id=action.id)
        
        self.assertEqual(self.morrison, action.actor)
        self.assertEqual(self.hendrix, action.target)
        self.assertEqual(self.lennon, action.action_object)

    def test_signals(self):
        handler = type('Handler', (object,), {
            'inc': lambda self: setattr(self, 'i', getattr(self, 'i') + 1),
            'i': 0
        })()
        
        def action_handler(instance, **kwargs):
            self.assertEqual(self.lennon, instance.actor)
            self.assertEqual(self.hendrix, instance.target)
            self.assertEqual(self.morrison, instance.action_object)
            handler.inc()
        
        signals.action.connect(action_handler)
            
        utils.action.send(self.lennon, 'follow', self.hendrix, action_object=self.morrison)
        
        self.assertEqual(1, handler.i)

    def test_template_tag(self):
        tpl = template.Template("""{% load stream_tags %}{% render_action action %}""")
        
        action = utils.action.send(self.lennon, 'default', self.hendrix)
        
        ctx = template.Context({'action': action})
        
        self.assertEqual("lennon did Stream Item hendrix.", tpl.render(ctx))
    
    def test_multi_lookups(self):
        def target_result():
            return len(Action.objects.get_for_targets([self.lennon, self.hendrix, self.morrison]))
        def actor_result():
            return len(Action.objects.get_for_actors([self.lennon, self.hendrix, self.morrison]))
        
        self.assertEqual(0, target_result())
        self.assertEqual(0, actor_result())
        
        utils.action.send(self.lennon, 'follow', self.hendrix)
        self.assertEqual(1, target_result())
        self.assertEqual(1, actor_result())

        utils.action.send(self.lennon, 'follow', self.morrison)
        self.assertEqual(2, target_result())
        self.assertEqual(2, actor_result())

        utils.action.send(self.hendrix, 'follow', self.morrison)
        self.assertEqual(3, target_result())
        self.assertEqual(3, actor_result())

        utils.action.send(self.hendrix, 'follow', self.lennon)
        self.assertEqual(4, target_result())
        self.assertEqual(4, actor_result())

        self.assertEqual(2, Action.objects.get_for_actors([self.lennon]).count())
        self.assertEqual(2, Action.objects.get_for_actors([self.hendrix]).count())
        self.assertEqual(0, Action.objects.get_for_actors([self.morrison]).count())
        
        self.assertEqual(1, Action.objects.get_for_targets([self.hendrix]).count())
        self.assertEqual(1, Action.objects.get_for_targets([self.lennon]).count())
        self.assertEqual(2, Action.objects.get_for_targets([self.morrison]).count())
