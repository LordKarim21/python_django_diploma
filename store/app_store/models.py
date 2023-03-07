from django.db import models
from datetime import datetime
from app_user.models import Profile


class Payment(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    month = models.IntegerField(default=datetime.now().month)
    year = models.IntegerField(default=datetime.now().year)
    number_card = models.IntegerField(null=True, blank=True)
