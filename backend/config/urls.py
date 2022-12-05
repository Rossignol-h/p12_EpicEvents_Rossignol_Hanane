from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path, include
from rest_framework import routers
from django.contrib import admin

from authentication.views import EmployeeViewSet
from client.views import ClientViewSet
from contract.views import ContractSalesViewSet

router = routers.DefaultRouter()
router.register('employees', EmployeeViewSet, basename='employee')
router.register('clients', ClientViewSet, basename='client')
router.register('contracts', ContractSalesViewSet, basename='contract')

urlpatterns = [

    path('admin/', admin.site.urls),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('crm/', include(router.urls))
]
