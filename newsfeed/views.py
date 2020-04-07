import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from friends.models import CustomNotification
from friends.serializers import NotificationSerializer
from .forms import PostForm
from .models import Post,Comment,User,Like,Dislike
from django.contrib import messages


# class PostCreateView(CreateView):
#     model = Post
#     form_class = PostForm
#     template_name = 'home.html'
#     success_url = reverse_lazy('core:home')

#     def form_valid(self, form):
#         if self.request.user.is_authenticated:
#             form.instance.user = self.request.user
#         return super(PostCreateView, self).form_valid(form)

#     def form_invalid(self, form):
#         """If the form is invalid, render the invalid form."""
#         print(form.errors)
#         return redirect(reverse_lazy('core:home'))

#     def post(self, *args, **kwargs):
#         form = self.get_form()
#         self.object = None
#         if form.is_valid():
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)


# def update_post(request,post_id):
#     post = Post.objects.get(id=post_id)
#     form = PostForm(instance = post)
#     if request.method =='POST':
#         form = PostForm(request.POST,request.FILES,request.user.profile,instance=post)
#         if form.is_valid():
#             form.save()
#             return reverse('core:home')

#     context = {'form':form}
#     return render(request,"newsfeed/udpatepost.html",context)

# def delete_post(request,post_id):
#     item = Post.objects.get(id=post_id)
#     if request.method=="POST":
#         item.delete()
#         return reverse('core:home')
#     context={'item':item}
#     return render(request,"newsfeed/postdelete.html",context)




# def postcreate(request):
#     posts = Post.objects.all()
#     form = PostForm()
#     if request.method=="POST":
#         form = PostForm(request.POST,request.FILES)
#         if form.is_valid():
#             if request.user.is_authenticated:
#                 form.instance.user = request.user
#             form.save()
#             return redirect('core:home')
#     context = {'posts':posts,'form':form}
#     return render(request, "home.html",context)




def create_comment(request, post_id=None):
    if request.method == "POST":
        post = Post.objects.get(id=post_id)
        comment = post.comments.create(user=request.user, content=request.POST.get('content'))
        notification = CustomNotification.objects.create(type="comment", recipient=post.user, actor=request.user, verb="commented on your post")
        channel_layer = get_channel_layer()
        channel = "comment_like_notifications_{}".format(post.user.username)
        print(json.dumps(NotificationSerializer(notification).data))
        async_to_sync(channel_layer.group_send)(
            channel, {
                "type": "notify",
                "command": "new_like_comment_notification",
                "notification": json.dumps(NotificationSerializer(notification).data)
            }
        )
        return redirect(reverse_lazy('core:home'))
    else:
        return redirect(reverse_lazy('core:home'))


class PostCreateView(CreateView):
  
 
    model = Post
   
    form_class = PostForm

    success_url = reverse_lazy('core:home')


    
    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
        return super(PostCreateView, self).form_valid(form)

class PostUpdateView( UpdateView):
    model = Post
    form_class = PostForm
  

    def test_func(self):  #to only allow author to update the post
        post = self.get_object()
        if(self.request.user==post.user):
            return True
        return False

# def PostUpdateView(request,pk):
#     if(request.method=='POST'):
#         post_form = PostForm(request.POST,request.FILES,instance=request.user)
    
#         if(post_form.is_valid()):
#             post_form.save()
            
#             messages.success(request, 'Your Post Successfully Updated')
#             return redirect('core:home')
#     else:
#             post_form = PostForm(instance=request.user,body = Post.objects.get(id=pk).body,post_image= Post.objects.get(id=pk).post_image.url)
            

    # context = {'post_form':post_form}
    # return render(request, "newsfeed/post_form.html",context)

class PostDeleteView( DeleteView):
    model = Post
    success_url = '/'


    def test_func(self):  #to only allow author to update the post
        post = self.get_object()
        if(self.request.user==post.user):
            return True
        return False

# def like_post(request, post_id):
#     if request.method=='POST':
#         post = Post.objects.get(id=post_id)
#         like = Like.objects.create(user=request.user)
#     return redirect(reverse_lazy('core:home'))

def like_post(request, post_id=None):
    if request.method == "POST":
        post = Post.objects.get(id=post_id)
        obj = Like.objects.filter(post=post,user = request.user)
        if not obj:
            like = post.likes.create(user=request.user)
        else :
            print("already liked")
        #like = post.likes.create(user=request.user)
        notification = CustomNotification.objects.create(type="like", recipient=post.user, actor=request.user, verb="liked your post")
        channel_layer = get_channel_layer()
        channel = "comment_like_notifications_{}".format(post.user.username)
        print(json.dumps(NotificationSerializer(notification).data))
        async_to_sync(channel_layer.group_send)(
            channel, {
                "type": "notify",
                "command": "new_like_comment_notification",
                "notification": json.dumps(NotificationSerializer(notification).data)
            }
        )
        return redirect(reverse_lazy('core:home'))
    else:
        return redirect(reverse_lazy('core:home'))


def dislike_post(request, post_id=None):
    if request.method == "POST":
        post = Post.objects.get(id=post_id)
        obj = Dislike.objects.filter(post=post,user = request.user)
        if not obj:
            like = post.dislikes.create(user=request.user)
        else :
            print("already disliked")
       # notification = CustomNotification.objects.create(type="dislike", recipient=post.user, actor=request.user, verb="disliked your post")
        #channel_layer = get_channel_layer()
        #channel = "comment_like_notifications_{}".format(post.user.username)
        #print(json.dumps(NotificationSerializer(notification).data))
        #async_to_sync(channel_layer.group_send)(
        #     channel, {
        #         "type": "notify",
        #         "command": "new_like_comment_notification",
        #         "notification": json.dumps(NotificationSerializer(notification).data)
        #     }
        # )
        return redirect(reverse_lazy('core:home'))
    else:
        return redirect(reverse_lazy('core:home'))