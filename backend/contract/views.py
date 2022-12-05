from rest_framework.permissions import DjangoModelPermissions
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework import filters

from .serializers import ContractManagerSerializer, ContractMemberSerializer, ContractStatusSerializer
from permissions import ObjectPermission
from .models import Contract, ContractStatus, ContractManager
from client.models import Client

# =========================================================== CONTRACT VIEW

class ContractSalesViewSet(viewsets.ModelViewSet):
    """
        Add, retrieve, update and delete a contract to the crm.
    """
    # serializer_class = ContractManagerSerializer
    # default_serializer_class = ContractMemberSerializer # Your default serializer
    serializer_class = ContractMemberSerializer
    queryset = Contract.objects.all()
    permission_classes = [DjangoModelPermissions, ObjectPermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ['date_created', 'amount', 'client_id__email', 'client_id__company_name' ]

    # def get_serializer_context(self):
    #     """
    #         Access to current user
    #     """
    #     context = super(ContractViewSet, self).get_serializer_context()
    #     context.update({"current_user": self.request.user})
    #     return context

    
    def override_contract(self, new_contract):
        ContractManager.objects.create(contract=new_contract)

        if self.request.data['status'] == 'True':
            ContractStatus.objects.create(contract=new_contract)
            current_client = Client.objects.get(id=self.request.data['client'])
            current_client.is_prospect = "False"
            current_client.save()


    def create(self, request, *args, **kwargs):
        # if self.request.user.is_superuser:
        #     self.serializer = self.serializer_class
        # else:
        #     self.serializer = self.default_serializer_class

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_contract = serializer.save()
        self.override_contract(new_contract)
        return Response({'new_contract': self.serializer(new_contract,
                            context=self.get_serializer_context()).data,
                            'message':
                            f"This new contract is successfully added to the crm."},
                            status=status.HTTP_201_CREATED)


    def update(self, request, *args, **kwargs):
        """
            if user change status of contract to True (is signed),
            update the client status (he is not a prospect anymore),
            & add this contract to table "ContractStatus".
        """
        current_contract = self.get_object()
        current_client_id = current_contract.client.id

        if request.data['status'] == 'True':
            ContractStatus.objects.create(contract=current_contract)
            Client.objects.update(id=str(current_client_id), is_prospect= "False")

        serializer = self.get_serializer(current_contract, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
    
        return Response(serializer.data)


    def destroy(self, request, *args, **kwargs):
        try:
            contract_to_delete = Contract.objects.get(id=self.kwargs['pk'])
            self.perform_destroy(contract_to_delete)
            return Response(
                        {'message': "This contract is successfully deleted"},
                        status=status.HTTP_204_NO_CONTENT)

        except ObjectDoesNotExist:
            raise ValidationError("This contract doesn't exist")


# =========================================================== CONTRACT VIEW


class ContractStatusViewSet(viewsets.ModelViewSet):
    """
    Add, retrieve, update and delete a contract status to the crm.
    """
    serializer_class = ContractStatusSerializer
    queryset = ContractStatus.objects.all()
    permission_classes = [DjangoModelPermissions, ObjectPermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ['contract',]
