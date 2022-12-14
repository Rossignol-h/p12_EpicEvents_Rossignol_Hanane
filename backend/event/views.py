from rest_framework.permissions import DjangoModelPermissions
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework import filters

from django.core.exceptions import ObjectDoesNotExist

from contract.models import ContractStatus
from .serializers import PartialEventSerializer, AllEventSerializer
from permissions import EventPermission

from authentication.models import Employee
from .models import Event


# ================================================================= EVENT VIEW


class ReadEventViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read & retrieve all events.
    """

    serializer_class = AllEventSerializer
    queryset = Event.objects.all()
    permission_classes = [DjangoModelPermissions]
    search_fields = ['event_date', 'client_id__email', 'client_id__company_name']
    filter_backends = (filters.SearchFilter,)


# ================================================================= EVENT VIEW


class EventViewSet(viewsets.ModelViewSet):
    """
    Add, retrieve, update and delete an event to the crm.
    """

    queryset = Event.objects.all()
    permission_classes = [DjangoModelPermissions, EventPermission]
    search_fields = ['event_date', 'client_id__email', 'client_id__company_name']
    filter_backends = (filters.SearchFilter,)

# ====================================================================== GET CONTRACTS OF AUTHENTICATED EMPLOYEE

    def get_serializer_class(self):
        if self.request.method == 'PUT' and self.request.user.is_superuser:
            return AllEventSerializer
        
        return PartialEventSerializer

# ===================================================================

    def get_contract(self, *args, **kwargs):
        return ContractStatus.objects.filter(contract=self.kwargs['contract_id']).first()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            if not self.get_contract():
                raise ObjectDoesNotExist()

            else:
                current_contract = self.get_contract()
                serializer.is_valid(raise_exception=True)
                new_event = serializer.save(
                    client=current_contract.contract.client,
                    event_status=current_contract
                )

                return Response({'new_event': serializer.data,
                                'message':
                                 'This new event is successfully added to the crm.'},
                                status=status.HTTP_201_CREATED)

        except ObjectDoesNotExist:
            raise ValidationError("This contract doesn't exist")


# ====================================================================== CUSTOM UPDATE EVENT

    def update(self, request, *args, **kwargs):
        """
            Support employee in charge of this event can update it,
            Manager can add the main support contact of this event.
        """

# ================================================================================ IF MANAGER ADD A SUPPORT CONTACT
        current_event = self.get_object()
        employee = request.user
        if employee.is_superuser:
            current_support = Employee.objects.filter(id=request.data['support_contact']).first()
        
            if not current_support:
                    response = {"Sorry, this support employee doesn't exist"}
                    return Response(response, status=status.HTTP_404_NOT_FOUND)

            else:
                current_event.support_contact = current_support
                current_event.save()
                serializer = self.get_serializer(current_event, data=request.data)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                return Response({'updated event': serializer.data,
                                'message':
                                f'This event is successfully updated, & the support contact is assigned to {current_support} '},
                                status=status.HTTP_201_CREATED)

        else:
            serializer = self.get_serializer(current_event, data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response({'updated event': serializer.data,
                                'message':
                                'This event is successfully updated.'},
                                status=status.HTTP_201_CREATED)


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
