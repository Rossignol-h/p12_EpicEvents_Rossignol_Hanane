from rest_framework.permissions import DjangoModelPermissions
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework import filters

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.http import Http404

from contract.models import ContractStatus
from .serializers import EventSerializer
from permissions import EventPermission
from .models import Event

# ================================================================= EVENT VIEW


class ReadEventsView(viewsets.ReadOnlyModelViewSet):
    """
    List all events.
    """
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    permission_classes = [DjangoModelPermissions]
    filter_backends = [filters.SearchFilter]
    search_fields = ['event_date', 'client_id__email', 'client_id__company_name']

# ================================================================= EVENT VIEW


class EventViewSet(viewsets.ModelViewSet):
    """
    Add, retrieve, update and delete an event to the crm.
    """

    serializer_class = EventSerializer
    queryset = Event.objects.all()
    permission_classes = [DjangoModelPermissions, EventPermission]
    search_fields = ['event_date', 'client_id', 'client_id.email']
    filter_backends = (filters.SearchFilter,)

    def get_contract(self):
        lookup_url_kwarg = self.kwargs['contract_id']
        return get_object_or_404(ContractStatus, pk=lookup_url_kwarg)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:

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
            raise Http404


    def destroy(self, request, *args, **kwargs):
        try:
            event_to_delete = Event.objects.get(id=self.kwargs['pk'])
            self.perform_destroy(event_to_delete)
            return Response(
                        {'message': "This event is successfully deleted"},
                        status=status.HTTP_204_NO_CONTENT)

        except ObjectDoesNotExist:
            raise ValidationError("This event doesn't exist")
