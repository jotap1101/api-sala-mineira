from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.translation import gettext_lazy as _
from drf_spectacular import utils
from rest_framework import exceptions, filters, parsers, permissions, response, status, viewsets
from utils.base_viewset import BaseViewSet
from .filters import CandidateFilter
from .serializers import *

# Create your views here.
@utils.extend_schema_view(
    list=utils.extend_schema(
        tags=['Candidate'],
        description=_('List all candidates.'),
        summary=_('List all candidates.'),
    ),
    create=utils.extend_schema(
        tags=['Candidate'],
        description=_('Create a new candidate.'),
        summary=_('Create a new candidate.'),
    ),
    retrieve=utils.extend_schema(
        tags=['Candidate'],
        description=_('Retrieve a candidate.'),
        summary=_('Retrieve a candidate.'),
    ),
    update=utils.extend_schema(
        tags=['Candidate'],
        description=_('Update a candidate.'),
        summary=_('Update a candidate.'),
    ),
    partial_update=utils.extend_schema(
        tags=['Candidate'],
        description=_('Partial update a candidate.'),
        summary=_('Partial update a candidate.'),
    ),
    destroy=utils.extend_schema(
        tags=['Candidate'],
        description=_('Delete a candidate.'),
        summary=_('Delete a candidate.'),
    )
)
class CandidateViewSet(BaseViewSet):
    queryset = Candidate.objects.all().order_by('id')
    serializer_class = CandidateSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CandidateFilter
    search_fields = ['first_name', 'last_name', 'cpf', 'rg']
    ordering_fields = ['-created_at', '-updated_at']
    ordering = ['-created_at']
    parser_classes = [parsers.JSONParser, parsers.MultiPartParser, parsers.FormParser]
    entity_name = 'Candidate'