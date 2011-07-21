from django.contrib.auth.models import User
from django.test import TestCase
from stream.models import Action

class TestStream(TestCase):
    def setUp(self):
        self.lennon = User.objects.create(username='lennon')
        self.hendrix = User.objects.create(username='hendrix')
        self.morrison = User.objects.create(username='morrison')
        
    def test_create(self):
        Action.objects.create(self.lennon, 'follow', self.hendrix)
        
        obj, created = Action.objects.get_or_create(self.lennon, 'follow', self.hendrix)
        self.assertEqual(False, created) 
    
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
        
        action = Action.objects.get(id=1)
        
        self.assertEqual(self.morrison, action.actor)
        self.assertEqual(self.hendrix, action.target)
        self.assertEqual(self.lennon, action.action_object)
