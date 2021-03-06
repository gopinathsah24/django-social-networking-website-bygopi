from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(
        'username',
        max_length=50,
        unique=True,
        help_text='Required. 50 characters or fewer. Letters, digits and @/./+/-/_ only.',
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    email = models.EmailField(unique=True, blank=False,
                              error_messages={
                                  'unique': "A user with that email already exists.",
                              })
    gender = models.CharField(max_length=20,choices=(('male','male'),('female','female')))
    status = models.BooleanField(default=False)
    about = models.CharField(max_length=400)
    firstname = models.CharField(max_length=50);
    lastname = models.CharField(max_length=20);

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "gender"]

    def __unicode__(self):
        return self.email
