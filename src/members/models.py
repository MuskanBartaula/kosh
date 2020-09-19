from django.db import models


class Member(models.Model):
    membership_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=120)
    number_of_share = models.PositiveIntegerField()

    def __str__(self):
        return self.name
