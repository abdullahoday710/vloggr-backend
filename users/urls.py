from django.urls import path
from rest_framework.authtoken import views
from .views import UserProfileRetrieveView, UserCreateView, UserProfileUpdateView, CurrentUserView,CreateFriendRequestView,AcceptFriendRequestView, DeclineFriendRequestView, FriendNotificationListView, FriendListView, ChangeProfilePicture,UpdateFcmTokenView
urlpatterns = [
    path('login/', views.obtain_auth_token),
    path('register/', UserCreateView.as_view()),
    path('update/<int:pk>', UserProfileUpdateView.as_view()),
    path('user/<int:pk>', UserProfileRetrieveView.as_view()),
    path('profile/', CurrentUserView.as_view()),
    path('add-friend/', CreateFriendRequestView.as_view()),
    path('accept-friend/<int:pk>', AcceptFriendRequestView.as_view(), name='accept-friend'),
    path('decline-friend/<int:pk>', DeclineFriendRequestView.as_view(), name='decline-friend'),
    path('friend-requests', FriendNotificationListView.as_view()),
    path('list-friends/', FriendListView.as_view()),
    path('change-profile-picture/<int:pk>', ChangeProfilePicture.as_view()),
    path('update-fcm-token/', UpdateFcmTokenView.as_view())
]
