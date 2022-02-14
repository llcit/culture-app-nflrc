from django.db import models
from culture_content.models import Profile
from datetime import datetime
from django.contrib.auth.models import User

lang_choices = (
    ('C', 'Chinese'),
    ('R', 'Russian'),
    ('A', 'Arabic'),
    ('L', 'All'),
    ('E', 'Russian-in-English'),
    ('B', 'Arabic-in-Arabic'),
		('P', 'Portuguese-in-English'),
    ('D', 'Portuguese-in-Portuguese'),
    ('F', 'French'),
    ('W', 'Swahili')
)


class Course(models.Model):
    name = models.CharField(max_length=150, blank=False)
    active = models.BooleanField(default=True)
    participants = models.ManyToManyField(Profile, blank=True)
    language = models.CharField (max_length=1, choices=lang_choices, blank=True)
    created = models.DateTimeField(max_length=100, default=datetime.now)
    created_by = models.CharField(max_length=50, blank=True)
    instructor = models.ManyToManyField(User, blank=True)
    enrollment_key = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.name







