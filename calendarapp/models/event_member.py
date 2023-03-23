from django.db import models

from django.contrib.auth.models import User
from calendarapp.models import Event, EventAbstract


class EventMember(EventAbstract):
    """ Event member model """

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="events")
    user = models.ManyToManyField(
        User,related_name="event_members"
    )


    def __str__(self):
        return str(self.user)
