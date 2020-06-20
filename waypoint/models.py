from django.db import models

# Create your models here.
class Waypoint(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=200)

    def __str__(self):
        return "WAYPOINT[ID={},CREATED={},UPDATED={},DESCRIPTION={}]".format(
                self.id, self.created, self.updated, self.description)

