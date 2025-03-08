from rest_framework import routers
from .views import UserViewSet

app_name = 'user'

router = routers.DefaultRouter()

router.register(prefix='users', viewset=UserViewSet, basename='user')

urlpatterns = router.urls
