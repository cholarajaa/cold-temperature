from django.conf.urls import url
from reactor.views import EventViewSet, aggregate_user_data
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'events', EventViewSet, base_name='events')


urlpatterns = [
    url(r'^userdata/update/$', aggregate_user_data),
] + router.urls
