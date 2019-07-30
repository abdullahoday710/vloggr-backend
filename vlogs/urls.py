from .views import CreateVlogView, ListVlogView
from django.urls import path

urlpatterns = [
    path('create-vlog/', CreateVlogView.as_view()),
    path('list-vlog/', ListVlogView.as_view()),
]
