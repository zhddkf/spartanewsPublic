from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    birth_date = models.DateField()
    gender = models.CharField(max_length=10, null=True, blank=True)

    def soft_delete(self):
        self.is_active = False
        self.save()
        return True

    def delete(self, using=None, keep_parents=False):
        self.soft_delete()
        return True