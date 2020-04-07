# import json

# from accounts.models import User
# from asgiref.sync import async_to_sync
# from channels.layers import get_channel_layer
# from django.http import JsonResponse
# from django.views.generic import ListView

# from .serializers import NotificationSerializer
# from .models import *
# from django.shortcuts import redirect


# # class FindFriendsListView(ListView):
# #     model = Friend
# #     context_object_name = 'users'
# #     template_name = "friends/find-friends.html"

# #     def get_queryset(self):
#         # si = self.request.GET.get("si")
#         # current_user_friends = self.request.user.friends.values('id')
#         # sent_request = list(Friend.objects.filter(user=self.request.user).values_list('friend_id', flat=True))
#         # if si==None:
#         #     si=""
#         # users = User.objects.exclude(id__in=current_user_friends).exclude(id__in=sent_request).exclude(id=self.request.user.id).filter(username__icontains=si)
#         # return users


# # def send_request(request, username=None):
# #     if username is not None:
# #         friend_user = User.objects.get(username=username)
# #         friend = Friend.objects.create(user=request.user, friend=friend_user)
# #         notification = CustomNotification.objects.create(type="friend", recipient=friend_user, actor=request.user, verb="sent you friend request")
# #         channel_layer = get_channel_layer()
# #         channel = "notifications_{}".format(friend_user.username)
# #         async_to_sync(channel_layer.group_send)(
# #             channel, {
# #                 "type": "notify",  # method name
# #                 "command": "new_notification",
# #                 "notification": json.dumps(NotificationSerializer(notification).data)
# #             }
# #         )
# #         data = {
# #             'status': True,
# #             'message': "Request sent.",
# #         }
# #         return JsonResponse(data)
# #     else:
# #         pass

# from django.shortcuts import redirect, render

# from .models import Friend

# # Create your views here.
# def FindFriendsListView(request):
#     users = User.objects.exclude(id=request.user.id)
    
#     si = request.GET.get("si")
#     if si==None:
#         si=""
#     users = User.objects.filter(username__icontains=si)
#     context = {
#         'users':users,
       
#     }

#     return render(request,'friends/find-friends.html',context)

# class FriendListView(ListView):
#     model = Friend
#     context_object_name = 'users'
#     template_name = "friends/timeline-friends.html"

#     def get_queryset(self):
#         #current_user_friends = self.request.user.friends.values('id')
#        # users = User.objects.filter(id__in = current_user_friends)
#         friend = Friend.objects.get(current_user=self.request.user.id)
#         friends = friend.users.all()
#         print(friends)
#         return friends

# def change_friend(request,operation,pk):
#     new_friend = User.objects.get(pk=pk)
#     if operation == 'add':
#         Friend.make_friend(request.user,new_friend)
#     elif operation == 'remove':
#         Friend.remove_friend(request.user,new_friend)
#     return redirect('core:home')


# def accept_request(request, friend=None):
#     if friend is not None:
#         friend_user = User.objects.get(username=friend)
#         current_user = request.user
#         f = Friend.objects.filter(user=friend_user, friend=current_user, status='requested')[0]
#         f.status = "friend"
#         f.save()
#         CustomNotification.objects.filter(recipient=current_user, actor=friend_user).delete()
#         data = {
#             'status': True,
#             'message': "You accepted friend request",
#         }
#         return JsonResponse(data)

# # def change_friend(request,operation,pk):
# #     new_friend = User.objects.get(pk=pk)
# #     if operation == 'add':
# #         Friend.make_friend(request.user,new_friend)
# #     elif operation == 'remove':
# #         Friend.remove_friend(request.user,new_friend)
# #     return redirect('home:home')

import json

from accounts.models import User
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import JsonResponse
from django.views.generic import ListView

from .serializers import NotificationSerializer
from .models import *


class FindFriendsListView(ListView):
    model = Friend
    context_object_name = 'users'
    template_name = "friends/find-friends.html"

    def get_queryset(self):
        si = self.request.GET.get("si")
        # current_user_friends = self.request.user.friends.values('id')
        current_user_friends = list(Friend.objects.filter(user = self.request.user,status="friend").values_list('friend_id',flat=True))
        sent_request = list(Friend.objects.filter(user=self.request.user,status="requested").values_list('friend_id', flat=True))
        if si==None:
            si=""
        users = User.objects.exclude(id__in=current_user_friends).exclude(id__in=sent_request).exclude(id=self.request.user.id).filter(username__icontains=si)
        return users
class FriendListView(ListView):
    model = Friend
    context_object_name = 'users'
    template_name = "friends/timeline-friends.html"

    def get_queryset(self):
        # current_user_friends = self.request.user.friends.values('id')
        # users = User.objects.filter(id__in = current_user_friends)
        current_user_friends = list(Friend.objects.filter(user = self.request.user,status="friend").values_list('friend_id',flat=True))
        users = User.objects.filter(id__in = current_user_friends)
        #users = User.objects.all()
        return users

def send_request(request, username=None):
    if username is not None:
        friend_user = User.objects.get(username=username)
        friend = Friend.objects.create(user=request.user, friend=friend_user,status="requested")
        notification = CustomNotification.objects.create(type="friend", recipient=friend_user, actor=request.user, verb="sent you friend request")
        channel_layer = get_channel_layer()
        channel = "notifications_{}".format(friend_user.username)
        async_to_sync(channel_layer.group_send)(
            channel, {
                "type": "notify",  # method name
                "command": "new_notification",
                "notification": json.dumps(NotificationSerializer(notification).data)
            }
        )
        data = {
            'status': True,
            'message': "Request sent.",
        }
        return JsonResponse(data)
    else:
        pass


def accept_request(request, friend=None):
    if friend is not None:
        friend_user = User.objects.get(username=friend)
        current_user = request.user
        f = Friend.objects.filter(user=friend_user, friend=current_user, status='requested')
        f.status = "friend"
        # f.save()
        CustomNotification.objects.filter(recipient=current_user, actor=friend_user).delete()
        data = {
            'status': True,
            'message': "You accepted friend request",
        }
        return JsonResponse(data)
