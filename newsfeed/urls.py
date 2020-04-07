from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
app_name = "newsfeed"

urlpatterns = [
    # path('',PostListView.as_view(),name="post-list"),
    path('post/create',PostCreateView.as_view(), name="post-create"),
    path('comment/create/<int:post_id>', create_comment, name="comment-create"),
    path('like/create/<int:post_id>', like_post, name="like_post"),
    path('dislike/create/<int:post_id>', dislike_post, name="dislike-post"),
    path('update_post/<int:pk>',PostUpdateView.as_view(),name="udpate-post"),
    path('delete_post/<int:pk>',PostDeleteView.as_view(),name="delete-post")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
