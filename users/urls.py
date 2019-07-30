from django.urls import path
from rest_framework.authtoken import views
from .views import UserProfileRetrieveView, UserCreateView, UserProfileUpdateView, FileUploadView, CurrentUserView,CreateFriendRequestView,AcceptFriendRequestView, DeclineFriendRequestView, FriendNotificationListView, UserSearchView
urlpatterns = [
    path('login/', views.obtain_auth_token),
    path('register/', UserCreateView.as_view()),
    path('update/<int:pk>', UserProfileUpdateView.as_view()),
    path('user/<int:pk>', UserProfileRetrieveView.as_view()),
    path('upload', FileUploadView.as_view()),
    path('profile/', CurrentUserView.as_view()),
    path('add-friend/', CreateFriendRequestView.as_view()),
    path('accept-friend/<int:pk>', AcceptFriendRequestView.as_view(), name='accept-friend'),
    path('decline-friend/<int:pk>', DeclineFriendRequestView.as_view(), name='decline-friend'),
    path('friend-requests', FriendNotificationListView.as_view()),
    path('search/', UserSearchView.as_view())
]
