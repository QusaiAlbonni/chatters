from rest_framework.routers import DefaultRouter

from .views import MessagesViewSet, RoomViewSet, LanguageViewSet

from rest_framework_nested.routers import NestedSimpleRouter

router = DefaultRouter()

router.register('rooms', RoomViewSet, 'rooms')
router.register('languages', LanguageViewSet, 'languages')

messages_router = NestedSimpleRouter(router, 'rooms', lookup='room')
messages_router.register('messages', MessagesViewSet, basename='messages')

urlpatterns = router.urls

urlpatterns += messages_router.urls