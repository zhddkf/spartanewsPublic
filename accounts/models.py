from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    email = models.EmailField(unique=True, blank=False)
    birth_date = models.DateField(blank=False)
    gender = models.CharField(max_length=10, null=True, blank=True)
    subscribings = models.ManyToManyField('self', symmetrical=False, related_name='subscribes')
    verification_token = models.CharField(max_length=255, blank=True, null=True)

    def soft_delete(self):
        self.is_active = False
        self.save()
        return True

    def delete(self, using=None, keep_parents=False):
        self.soft_delete()
        return True

    def __str__(self):
        return str(self.username)