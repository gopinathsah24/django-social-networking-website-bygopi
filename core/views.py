from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.db.models import Q
from friends.models import CustomNotification
from friends.models import Friend
from newsfeed.models import Post
from communications.models import Message

def home(request):
    if not request.user.is_authenticated:
        return redirect(reverse_lazy('accounts:login'))

    friends_one = Friend.objects.filter(friend=request.user).filter(status='friend')
    friends_two = Friend.objects.filter(user=request.user).filter(status='friend')
    friends_list_one = list(friends_one.values_list('user_id', flat=True))
    friends_list_two = list(friends_two.values_list('friend_id', flat=True))
    friends_list_id =  friends_list_two + [request.user.id]
    friends = friends_one.union(friends_two)
    posts = Post.objects.filter(user__in=friends_list_id)
    notifications = CustomNotification.objects.filter(recipient=request.user,deleted=False)[0:5]
    messages = Message.objects.filter(friend=request.user)[0:5]
    # friend = Friend.objects.get(current_user=request.user.id)
    # friends = friend.users.all()
    #posts = Post.objects.all().order_by('-created_at')
    return render(request, "home.html", {'posts': posts, 'friends': friends,'notifications':notifications,'messages':messages})
