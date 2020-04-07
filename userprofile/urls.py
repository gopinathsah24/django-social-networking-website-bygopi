from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = "profile"

urlpatterns = [
    path('edit-profile', ProfileEditView, name="edit-profile"),
    path('<slug:username>', TimelineView.as_view(), name="user-timeline"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
