from typing import Optional
from typing import Any
from django.contrib.auth.backends import ModelBackend
from rest_framework.permissions import IsAuthenticated as BaseIsAuthenticated
from rest_framework.request import Request
from rest_framework.views import APIView
from users.models import User
from django.db.models import Q


class AuthenticationBackend(ModelBackend):
    """Custom authentication backend that also checks for the `is_deleted` status."""

    def user_can_authenticate(self, user: Optional[User]) -> bool:  # type: ignore # Use our User
        not_deleted = not getattr(user, "is_deleted", False)
        return not_deleted and super().user_can_authenticate(user)

    """Override and replicate the super method, adding the possibility to login via email or contact."""

    def authenticate(self, request: Any, username: Any = None, password: Any = None, **kwargs: Any) -> Optional[User]:
        
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)
        if username is None or password is None:
            return None
        try:
            user = User.objects.filter(Q(email=username) | Q(username=username)).get()
        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760), replicating the super method
            User().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        return None

class AuthenticatedRequest(Request):
    """Authenticated class to correctly type the user in requests."""

    user: User


class IsAuthenticated(BaseIsAuthenticated):
    """Modify the IsAuthenticated permission to block inactive and deleted users."""

    def has_permission(self, request: AuthenticatedRequest, view: APIView) -> bool:  # type: ignore # Use our User
        return super().has_permission(request, view) and request.user.is_active and not request.user.is_deleted


class IsStaff(IsAuthenticated):
    """Extend the `IsAuthenticated` permission to only allow users with `is_staff == True`."""

    def has_permission(self, request: AuthenticatedRequest, view: APIView) -> bool:  # type: ignore # Use our User
        return super().has_permission(request, view) and request.user.is_staff
