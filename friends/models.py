# from django.conf import settings
# from django.db import models

# from accounts.models import User
# from django.utils.timezone import now


# # class Friend(models.Model):
# #     user = models.ForeignKey(User, on_delete=models.CASCADE)  # who sent the request
# #     #friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends')
# #     friend = models.ManyToManyField(User,on_delete=models.CASCADE,related_name='friends')  # who will receive the request
# #     # sender = models.CharField(max_length=20, default='requested')
# #     status = models.CharField(max_length=20, default='requested')
# #     created_at = models.DateTimeField(default=now)
    
    

    

# from django.db import models

# from django.db.models import CASCADE
# # Create your models here.

# class Friend(models.Model):
#     users = models.ManyToManyField(User)
#     current_user = models.ForeignKey(User,related_name="owner",on_delete=CASCADE,null=True)

#     @classmethod
#     def make_friend(cls,current_user,new_friend):
#         friend,created = cls.objects.get_or_create(current_user=current_user)
#         friend.users.add(new_friend)

#     @classmethod
#     def remove_friend(cls,current_user,new_friend):
#         friend,created = cls.objects.get_or_create(current_user=current_user)
#         friend.users.remove(new_friend)






# class CustomNotification(models.Model):
#     type = models.CharField(default='friend', max_length=30)

#     recipient = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         blank=False,
#         related_name='notifications',
#         on_delete=models.CASCADE
#     )
#     unread = models.BooleanField(default=True, blank=False, db_index=True)

#     actor = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         blank=False,
#         on_delete=models.CASCADE
#     )

#     verb = models.CharField(max_length=255)
#     description = models.TextField(blank=True, null=True)

#     timestamp = models.DateTimeField(default=now, db_index=True)

#     deleted = models.BooleanField(default=False, db_index=True)
#     emailed = models.BooleanField(default=False, db_index=True)


from django.conf import settings
from django.db import models

from accounts.models import User
from django.utils.timezone import now


class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # who sent the request
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends')  # who will receive the request
    # sender = models.CharField(max_length=20, default='requested')
    status = models.CharField(max_length=20, default='notrequested')
    created_at = models.DateTimeField(default=now)


class CustomNotification(models.Model):
    type = models.CharField(default='friend', max_length=30)

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=False,
        related_name='notifications',
        on_delete=models.CASCADE
    )
    unread = models.BooleanField(default=True, blank=False, db_index=True)

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=False,
        on_delete=models.CASCADE
    )

    verb = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    timestamp = models.DateTimeField(default=now, db_index=True)

    deleted = models.BooleanField(default=False, db_index=True)
    emailed = models.BooleanField(default=False, db_index=True)