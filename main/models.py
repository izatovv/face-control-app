from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photos/', blank=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Profile for user {self.user.username}'

    def empty_fields(self):
        fields = [
            self.photo,
            self.phone_number,
            self.country,
            self.full_name,
            self.user.email
        ]
        print(fields)
        empty_count = sum(
            field is None or (isinstance(field, str) and len(field.strip()) == 0)
            for field in fields
        )
        return empty_count

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
        db_table = 'profiles'
