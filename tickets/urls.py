from rest_framework.routers import DefaultRouter
from .views import (
    TheatreHallViewSet, GenreViewSet, ActorViewSet,
    PlayViewSet, PerformanceViewSet, ReservationViewSet
)

router = DefaultRouter()
router.register("halls", TheatreHallViewSet)
router.register("genres", GenreViewSet)
router.register("actors", ActorViewSet)
router.register("plays", PlayViewSet)
router.register("performances", PerformanceViewSet)
router.register("reservations", ReservationViewSet, basename="reservations")

urlpatterns = router.urls
