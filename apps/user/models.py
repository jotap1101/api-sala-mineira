from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from utils.generate_hashed_filename import upload_to
from uuid import uuid4
import os

# Create your models here.
class User(AbstractUser):
    class Meta:
        db_table = 'auth_user'
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def profile_picture_upload_to(instance, filename):
        return upload_to(instance, filename, 'users/profile_pictures')

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, verbose_name=_('ID'))
    email = models.EmailField(unique=True, verbose_name=_('E-mail'))
    profile_picture = models.ImageField(upload_to=profile_picture_upload_to, null=True, blank=True, verbose_name=_('Profile picture'))

    def save(self, *args, **kwargs):
        if self.pk:
            try:
                old_instance = User.objects.get(pk=self.pk)
                if old_instance.profile_picture and old_instance.profile_picture != self.profile_picture:
                    if os.path.isfile(old_instance.profile_picture.path):
                        os.remove(old_instance.profile_picture.path)
            except User.DoesNotExist:
                pass

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.profile_picture:
            if os.path.isfile(self.profile_picture.path):
                os.remove(self.profile_picture.path)

        super().delete(*args, **kwargs)

    def __str__(self):
        return self.get_full_name() or self.username