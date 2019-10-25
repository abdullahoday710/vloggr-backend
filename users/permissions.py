from rest_framework.permissions import BasePermission
from .models import UserProfile
class IsOwnerOrReadOnly(BasePermission):
      message = "You must be the owner of this profile to edit it."
      def has_object_permission(self, request, view, obj):
          return obj.user == request.user
