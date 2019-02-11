from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register('user',EmployeeViewSet)

urlpatterns = [
    path('/',include(router.urls)),
]