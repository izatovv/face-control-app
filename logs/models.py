from django.db import models
from main.models import Profile


class Log(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='logs')
    photo = models.ImageField(upload_to='logs/', blank=True)
    is_correct = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Log'
        verbose_name_plural = 'Logs'
        db_table = 'logs'
