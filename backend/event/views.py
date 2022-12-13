from rest_framework.permissions import DjangoModelPermissions
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework import filters

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.http import Http404

from contract.models import ContractStatus
from .serializers import PartialEventSerializer, AllEventSerializer
from permissions import EventPermission
from .models import Event


# ================================================================= EVENT VIEW


class ReadEventViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read & retrieve all events.
    """

    serializer_class = AllEventSerializer
    queryset = Event.objects.all()
    permission_classes = [DjangoModelPermissions]
    search_fields = ['event_date', 'client_id', 'client_id.email']
    filter_backends = (filters.SearchFilter,)


# ================================================================= EVENT VIEW


class EventViewSet(viewsets.ModelViewSet):
    """
    Add, retrieve, update and delete an event to the crm.
    """

    serializer_class = AllEventSerializer
    queryset = Event.objects.all()
    permission_classes = [DjangoModelPermissions, EventPermission]
    search_fields = ['event_date', 'client_id', 'client_id.email']
    filter_backends = (filters.SearchFilter,)


# ====================================================================== GET CONTRACTS OF AUTHENTICATED EMPLOYEE

    def get_serializer_class(self):
        if self.request.method == 'PUT' and self.request.user.is_superuser:
            return AllEventSerializer
        elif self.request.method == 'PUT' and self.request.user.role == 'sales':
            return PartialEventSerializer

# =================================================================== 

    def get_contract(self, *args, **kwargs):
        return ContractStatus.objects.get(contract=self.kwargs['contract_id'])

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            if not self.get_contract():
                raise ValidationError("this contract doesn't exist")
                
            else:
                current_contract = self.get_contract()
                serializer.is_valid(raise_exception=True)
                new_event = serializer.save(
                            client=current_contract.contract.client, 
                            event_status=current_contract
                            )

                return Response({
                    'New event': EventSerializer(new_event, context=self.get_serializer_context()).data,
                    'message': f"this event is successfully added to the crm"},
                    status=status.HTTP_201_CREATED)
                
        except ObjectDoesNotExist:
            raise ValidationError("This event doesn't exist")

# =================================================================== 


    def destroy(self, request, *args, **kwargs):
        try:
            event_to_delete = Event.objects.get(id=self.kwargs['pk'])
            self.perform_destroy(event_to_delete)
            return Response(
                        {'message': "This event is successfully deleted"},
                        status=status.HTTP_204_NO_CONTENT)

        except ObjectDoesNotExist:
            raise ValidationError("This event doesn't exist")
