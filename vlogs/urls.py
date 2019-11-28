from .views import (CreateVlogView,
ListMediaView,
ListSharedWithVlogView,
CreateAlbumView,
UpdateVlogView,
CreatePhotoView,)
from django.urls import path

urlpatterns = [
    path('create-vlog/', CreateVlogView.as_view()),
    path('list-media/', ListMediaView.as_view()),
    path('shared-with-me/',ListSharedWithVlogView.as_view()),
    path('create-album/',CreateAlbumView.as_view()),
    path('update-vlog/<int:pk>',UpdateVlogView.as_view()),
    path('create-photo/', CreatePhotoView.as_view()),
]
