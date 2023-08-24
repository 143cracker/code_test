from codetest.views import FetchApiView
from django.urls import path,include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api/fetch-pack',FetchApiView,basename="fetch-api")


urlpatterns = [
    path('',include(router.urls))
]
