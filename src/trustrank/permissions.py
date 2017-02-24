from django.utils import timezone
from rest_framework import permissions

class IsOwnerAndNewData(permissions.BasePermission):
    """
    Custom permission allows users to edit or delete objects they've created for
    30 minutes.  After 30 minutes, objects are read-only for everybody.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the creator of the object
        if obj.added_by == request.user.profile:
            # Write permissions are only allowed for 30 minutes after creation.
            if (timezone.now() - obj.date_added).seconds < 1800:
                return True
        return False
