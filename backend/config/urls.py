from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework import routers
from django.conf import settings
from django.contrib import admin

from authentication.views import EmployeeViewSet
from client.views import ClientViewSet
from contract.views import ContractViewSet, ContractStatusViewSet
from event.views import EventViewSet, ReadEventViewSet

router = routers.DefaultRouter()
router.register('employees', EmployeeViewSet, basename='employee')
router.register('clients', ClientViewSet, basename='clients')

router.register('contracts', ContractViewSet, basename='contracts')
router.register('signed_contracts', ContractStatusViewSet, basename='contracts')

router.register("events", ReadEventViewSet, basename="events")
router.register(r"^(?P<contract_id>[^/.]+)/events", EventViewSet, basename="event")

# For customized admin page's title
admin.site.index_title = 'Welcome to the CRM of EpicEvents'

urlpatterns = [

    path('admin/', admin.site.urls),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('crm/', include(router.urls))
]

# ================================================================ STATIC/MEDIA

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
