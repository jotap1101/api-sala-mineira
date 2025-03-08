from rest_framework import routers
from .views import CandidateViewSet

app_name = 'candidate'

router = routers.DefaultRouter()

router.register(prefix='candidates', viewset=CandidateViewSet, basename='candidate')

urlpatterns = router.urls