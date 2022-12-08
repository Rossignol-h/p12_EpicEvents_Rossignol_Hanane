from rest_framework.permissions import DjangoModelPermissions
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework import filters

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.http import Http404

from .serializers import ContractSerializer, ContractStatusSerializer
from permissions import ObjectPermission
from .models import Contract, ContractStatus
from client.models import Client


# =========================================================== READ CONTRACT VIEW


class ReadContractsView(viewsets.ReadOnlyModelViewSet):
    """
    List all contracts.
    """
    serializer_class = ContractSerializer
    queryset = Contract.objects.all()
    permission_classes = [DjangoModelPermissions]
    filter_backends = [filters.SearchFilter]
    search_fields = ['date_created', 'amount', 'client_id__email', 'client_id__company_name' ]

# =========================================================== CONTRACT VIEW


class ContractView(viewsets.ModelViewSet):
    """
        Add, retrieve, update and delete a contract to the crm.
    """
    serializer_class = ContractSerializer
    # queryset = Contract.objects.all()
    permission_classes = [DjangoModelPermissions, ObjectPermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ['date_created', 'amount', 'client_id__email', 'client_id__company_name' ]


    def get_client(self):
        lookup_url_kwarg = self.kwargs['client_id']
        return get_object_or_404(Client, pk=lookup_url_kwarg)


# ====================================================================== GET CONTRACTS OF AUTHENTICATED EMPLOYEE


    def get_queryset(self):
        employee = self.request.user
        if employee.role == 'sales':
            return Contract.objects.filter(sales_contact=employee)
        elif employee.role == 'support':
            return Contract.objects.filter(event__support_contact=employee)
        elif employee.is_superuser:
            return Contract.objects.all()
        else:
            return Contract.objects.none()

# ====================================================================== METHOD FOR ADD SIGNED CONTRACT & CHANGE PROSPECT TO CLIENT


    def update_foreignkeys(self, new_contract):

        if self.request.data['status'] == 'True':

            signed_contract = ContractStatus.objects.filter(contract=new_contract)
            if signed_contract:
                pass
            else: 
                ContractStatus.objects.create(contract=new_contract)
            
            current_client = self.get_client()
            if current_client:
                current_client.is_prospect = "False"
                current_client.save()
        else:
            if signed_contract:
                ContractStatus.objects.delete(contract=new_contract)
            else:
                pass
# ====================================================================== CUSTOM CREATE CONTRACT

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        current_client = self.get_client()
        new_contract = serializer.save(
                                    client=current_client,
                                    sales_contact=current_client.sales_contact
                                    )

        self.update_foreignkeys(new_contract)

        return Response({'new_contract': self.serializer_class(new_contract,
                            context=self.get_serializer_context()).data,
                            'message':
                            f"This new contract is successfully added to the crm."},
                            status=status.HTTP_201_CREATED)


# ====================================================================== CUSTOM UPDATE CONTRACT


    def update(self, request, *args, **kwargs):
        """
            if user change status of contract to True (is signed),
            update the client status (he is not a prospect anymore),
            & add this contract to table "ContractStatus".
        """
        current_contract = self.get_object()
        serializer = self.get_serializer(current_contract, data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        self.update_foreignkeys(current_contract)
    
        return Response(serializer.data)

# ====================================================================== METHOD TO DISPLAY DELETE MESSAGE


    def destroy(self, request, *args, **kwargs):
        try:
            contract_to_delete = Contract.objects.get(id=self.kwargs['pk'])
            self.perform_destroy(contract_to_delete)
            return Response(
                        {'message': "This contract is successfully deleted"},
                        status=status.HTTP_204_NO_CONTENT)

        except ObjectDoesNotExist:
            raise ValidationError("This contract doesn't exist")


# =========================================================== SIGNED CONTRACT VIEW


class ContractStatusViewSet(viewsets.ModelViewSet):
    """
    Add, retrieve, update and delete a contract status to the crm.
    """
    serializer_class = ContractStatusSerializer
    queryset = ContractStatus.objects.all()
    permission_classes = [DjangoModelPermissions, ObjectPermission]
