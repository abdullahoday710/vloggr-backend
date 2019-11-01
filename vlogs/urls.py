from .views import CreateVlogView, ListVlogView,ListSharedWithVlogView
from django.urls import path

urlpatterns = [
    path('create-vlog/', CreateVlogView.as_view()),
    path('list-vlog/', ListVlogView.as_view()),
    path('shared-with-me/',ListSharedWithVlogView.as_view()),
]
