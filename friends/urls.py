# from django.urls import path
# from .views import *

# app_name = "friends"

# urlpatterns = [
#     path('find-friends', FindFriendsListView, name="find-friends"),
#     path('friends', FriendListView.as_view(), name="my_friends"),
#     # path('send-request/<slug:username>', send_request, name="send-request"),
#     path('change/<str:operation>/<int:pk>',change_friend,name='change_friend'),
#     path('accept-request/<slug:friend>', accept_request, name="accept-request"),
# ]

from django.urls import path
from .views import *

app_name = "friends"

urlpatterns = [
    path('find-friends', FindFriendsListView.as_view(), name="find-friends"),
    path('friends', FriendListView.as_view(), name="my_friends"),
    path('send-request/<slug:username>', send_request, name="send-request"),
    path('accept-request/<slug:friend>', accept_request, name="accept-request"),
]
