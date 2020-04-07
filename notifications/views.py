from django.http import JsonResponse
from django.shortcuts import redirect, render

from friends.models import CustomNotification
from django.urls import reverse_lazy


def mark_like_comment_notifications_as_read(request):
    CustomNotification.objects.filter(recipient=request.user, type="comment").update(unread=False)
    return JsonResponse({
        'status': True,
        'message': "Marked all notifications as read"
    })


def notifications_home(request):
    notifications = CustomNotification.objects.filter(recipient=request.user)
    return render(request,'notifications/notifications.html',{'notifications':notifications})

def notification_delete(request,pk):
    notification = CustomNotification.objects.get(id=pk)
    if request.method=="POST":
        notification.delete()
        return redirect(reverse_lazy('notifications:notifications'))
    return render(request,'notifications/notifications_delete.html',{'notifications':notification})
