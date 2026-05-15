from rest_framework.routers import DefaultRouter
from .views import WorkflowCaseViewSet
router=DefaultRouter(); router.register('cases',WorkflowCaseViewSet)
urlpatterns=router.urls
