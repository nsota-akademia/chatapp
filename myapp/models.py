from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.


class CustomUser(AbstractUser):
    file = models.ImageField(upload_to="")  # media_rootに対する相対パスを入力
    email = models.EmailField(_("email address"), blank=True, unique=True)


class Messages(models.Model):
    message_from = models.IntegerField()
    message_to = models.IntegerField()
    message = models.CharField(max_length=2000)
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
