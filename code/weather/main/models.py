from django.contrib.auth.models import User
from django.db import models
from django.core.validators import URLValidator
from django.db.models import Manager


# Create your models here.


class User_data(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='data', default=None, null=True)
    last_user_request = models.URLField(validators=[URLValidator(schemes=['https'])])

    def __str__(self):
        return f""

    def __repr__(self):
        return f""

    objects = Manager()


class Stats(models.Model):
    id = models.AutoField(primary_key=True)
    city = models.CharField(max_length=60, unique=True, )
    count_requests = models.IntegerField(default=0, null=False)

    def __str__(self):
        return f"Statistics of {self.city}"

    def __repr__(self):
        return f"{self.city} is requested {self.count_requests}"

    objects = Manager()
