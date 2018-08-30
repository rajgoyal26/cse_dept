from django.db import models
from enum import Enum
from user.models import User
#from events.models import Event

class PlacementType(Enum):
    OFC = "Off Campus"
    ONC = "On Campus"


class Industry(models.Model):
    name = models.CharField(max_length=50)
    year = models.PositiveSmallIntegerField()  #year of establishment
    area_of_operation = models.TextField()
    comments = models.TextField()
    contact_number = models.CharField(max_length=10)
    mail = models.EmailField()


class StudentPlacement(models.Model):
    student = models.ForeignKey(User, on_delete=None)
    industry = models.ForeignKey(Industry, on_delete=None)
    package = models.BigIntegerField()
    date_of_visit = models.DateField()
    date_of_joining = models.DateField()
    attachment = models.FileField()
    location = models.TextField()
    type = [(tag, tag.value) for tag in PlacementType ]
    #status = models.CharField(max_length=)
    #event = models.ForeignKey(Event, on_delete=None)


class PlacementFeedback(models.Model):
    student = models.ForeignKey(User, on_delete=None)
    industry = models.ForeignKey(Industry, on_delete=None)
    active = models.BooleanField()
    # event = models.ForeignKey(Event, on_delete=None)
    #forum = models.ForeignKey(Forum, on_delete=None)


class IndustryInteraction(models.Model):
    industry = models.ForeignKey(Industry, on_delete=None)
    date = models.DateField()
    person = models.TextField()
