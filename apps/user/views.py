from django.contrib.auth import get_user_model
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.translation import gettext_lazy as _
from drf_spectacular import utils
from rest_framework import exceptions, filters, parsers, permissions, response, status, viewsets
from utils.base_viewset import BaseViewSet
from .permissions import IsRegularUser, IsStaffUser, IsSuperUser
from .serializers import UserSerializer

# Create your views here.
User = get_user_model()

@utils.extend_schema_view(
    list=utils.extend_schema(
        tags=['User'],
        description=_('List all users.'),
        summary=_('List all users.'),
    ),
    create=utils.extend_schema(
        tags=['User'],
        description=_('Create a new user.'),
        summary=_('Create a new user.'),
    ),
    retrieve=utils.extend_schema(
        tags=['User'],
        description=_('Retrieve a user.'),
        summary=_('Retrieve a user.'),
    ),
    update=utils.extend_schema(
        tags=['User'],
        description=_('Update a user.'),
        summary=_('Update a user.'),
    ),
    partial_update=utils.extend_schema(
        tags=['User'],
        description=_('Partial update a user.'),
        summary=_('Partial update a user.'),
    ),
    destroy=utils.extend_schema(
        tags=['User'],
        description=_('Delete a user.'),
        summary=_('Delete a user.'),
    )
)
class UserViewSet(BaseViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'is_staff', 'is_superuser']
    search_fields = ['username', 'email']
    ordering_fields = ['id', 'username', 'email', 'is_active', 'is_staff', 'is_superuser']
    ordering = ['id']
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser, parsers.FormParser]
    entity_name = 'User'

    def get_permissions(self):
        match self.action:
            case 'list':
                self.permission_classes = [permissions.IsAuthenticated, IsSuperUser | IsStaffUser]
            case 'create':
                self.permission_classes = [permissions.IsAuthenticated, IsSuperUser]
            case 'retrieve':
                self.permission_classes = [permissions.IsAuthenticated, IsSuperUser | IsStaffUser | IsRegularUser]
            case 'update':
                self.permission_classes = [permissions.IsAuthenticated, IsSuperUser | IsStaffUser | IsRegularUser]
            case 'partial_update':
                self.permission_classes = [permissions.IsAuthenticated, IsSuperUser | IsStaffUser | IsRegularUser]
            case 'destroy':
                self.permission_classes = [permissions.IsAuthenticated, IsSuperUser]
            case _:
                self.permission_classes = [permissions.IsAuthenticated]

        return [permission() for permission in self.permission_classes]