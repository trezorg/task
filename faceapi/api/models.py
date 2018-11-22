from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):

    email = models.EmailField(
        _('Email'),
        blank=False,
        null=False,
        unique=True,
    )

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'


class FacebookPage(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='user',
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )
    access_token = models.TextField(
        _('Access Token'),
        null=False,
        blank=False,
    )


class FacebookLabel(models.Model):

    page = models.ForeignKey(
        FacebookPage,
        related_name='page',
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )
    label_id = models.TextField(
        _('Label ID'),
        null=False,
        blank=False,
    )
    label = models.TextField(
        _('Label'),
        null=False,
        blank=False,
        unique=True,
    )
