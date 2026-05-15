from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from apps.accounts.views import MyTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/auth/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/accounts/', include('apps.accounts.urls')),
    path('api/customers/', include('apps.customers.urls')),
    path('api/documents/', include('apps.documents.urls')),
    path('api/verification/', include('apps.verification.urls')),
    path('api/risk/', include('apps.risk.urls')),
    path('api/workflow/', include('apps.workflow.urls')),
    path('api/cases/', include('apps.cases.urls')),
    path('api/dashboards/', include('apps.dashboards.urls')),
    path('api/audit/', include('apps.audit.urls')),
    path('api/communications/', include('apps.communications.urls')),
    path('api/integrations/', include('apps.integrations.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
