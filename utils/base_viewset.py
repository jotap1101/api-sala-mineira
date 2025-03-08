from django.http import Http404
from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets, status, exceptions, response

class BaseViewSet(viewsets.ModelViewSet):
    entity_name = "Entity"  # Esse atributo será sobrescrito pelas subclasses

    def get_entity_name(self):
        return self.entity_name

    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except Exception:
            raise exceptions.APIException(
                detail=_('An error occurred while listing {entity}.').format(entity=self.get_entity_name()),
                code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def create(self, request, *args, **kwargs):
        try:
            res = super().create(request, *args, **kwargs)
            return response.Response(
                data={
                    'message': _('{} created successfully.').format(self.get_entity_name()),
                    'data': res.data
                },
                status=status.HTTP_201_CREATED
            )
        except exceptions.ValidationError as e:
            raise exceptions.ValidationError(
                detail={
                    'message': _('An error occurred while creating {}.').format(self.get_entity_name()),
                    'errors': e.detail
                },
                code=status.HTTP_400_BAD_REQUEST
            )
        except Exception:
            raise exceptions.APIException(
                detail=_('An error occurred while creating {}.').format(self.get_entity_name()),
                code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def retrieve(self, request, *args, **kwargs):
        try:
            res = super().retrieve(request, *args, **kwargs)
            
            return response.Response(
                data={
                    'message': _('{} retrieved successfully.').format(self.get_entity_name()),
                    'data': res.data
                },
                status=status.HTTP_200_OK
            )
        except Http404:
            raise exceptions.NotFound(
                detail=_('{} not found.').format(self.get_entity_name()),
                code=status.HTTP_404_NOT_FOUND
            )
        except Exception:
            raise exceptions.APIException(
                detail=_('An error occurred while retrieving {}.').format(self.get_entity_name()),
                code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def update(self, request, *args, **kwargs):
        try:
            res = super().update(request, *args, **kwargs)
            return response.Response(
                data={
                    'message': _('{} updated successfully.').format(self.get_entity_name()),
                    'data': res.data
                },
                status=status.HTTP_200_OK
            )
        except Http404:
            raise exceptions.NotFound(
                detail=_('{} not found.').format(self.get_entity_name()),
                code=status.HTTP_404_NOT_FOUND
            )
        except exceptions.ValidationError as e:
            raise exceptions.ValidationError(
                detail={
                    'message': _('An error occurred while updating {}.').format(self.get_entity_name()),
                    'errors': e.detail
                },
                code=status.HTTP_400_BAD_REQUEST
            )
        except Exception:
            raise exceptions.APIException(
                detail=_('An error occurred while updating {}.').format(self.get_entity_name()),
                code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def partial_update(self, request, *args, **kwargs):
        try:
            res = super().partial_update(request, *args, **kwargs)
            return response.Response(
                data={
                    'message': _('{} partially updated successfully.').format(self.get_entity_name()),
                    'data': res.data
                },
                status=status.HTTP_200_OK
            )
        except Http404:
            raise exceptions.NotFound(
                detail=_('{} not found.').format(self.get_entity_name()),
                code=status.HTTP_404_NOT_FOUND
            )
        except exceptions.ValidationError as e:
            raise exceptions.ValidationError(
                detail={
                    'message': _('An error occurred while updating {}.').format(self.get_entity_name()),
                    'errors': e.detail
                },
                code=status.HTTP_400_BAD_REQUEST
            )
        except Exception:
            raise exceptions.APIException(
                detail=_('An error occurred while updating {}.').format(self.get_entity_name()),
                code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def destroy(self, request, *args, **kwargs):
        try:
            res = super().destroy(request, *args, **kwargs)
            return response.Response(
                data={'message': _('{} deleted successfully.').format(self.get_entity_name())},
                status=status.HTTP_204_NO_CONTENT
            )
        except Http404:
            raise exceptions.NotFound(
                detail=_('{} not found.').format(self.get_entity_name()),
                code=status.HTTP_404_NOT_FOUND
            )
        except Exception:
            raise exceptions.APIException(
                detail=_('An error occurred while deleting {}.').format(self.get_entity_name()),
                code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
