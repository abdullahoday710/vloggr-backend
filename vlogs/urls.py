from .views import CreateVlogView, ListVlogView, ListSharedWithVlogView, CreateAlbumView, UpdateVlogView
from django.urls import path

urlpatterns = [
    path('create-vlog/', CreateVlogView.as_view()),
    path('list-vlog/', ListVlogView.as_view()),
    path('shared-with-me/',ListSharedWithVlogView.as_view()),
    path('create-album/',CreateAlbumView.as_view()),
    path('update-vlog/<int:pk>',UpdateVlogView.as_view())
]
