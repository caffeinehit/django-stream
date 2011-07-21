from django.db import models

# Create your models here.

from django.contrib.auth.models import User, Group
from stream import utils


utils.register_actor([User, Group])
utils.register_target([User, Group])
utils.register_action_object([User, Group])
