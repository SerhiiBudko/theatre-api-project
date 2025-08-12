from django.db import transaction, IntegrityError
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import TheatreHall, Genre, Actor, Play, Performance, Reservation, Ticket
from .serializers import (
    TheatreHallSerializer, GenreSerializer, ActorSerializer,
    PlaySerializer, PerformanceSerializer,
    ReservationSerializer, CreateReservationSerializer
)

# простий пермішн: адміни можуть змінювати, інші — тільки читати
from rest_framework.permissions import BasePermission, SAFE_METHODS
class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (request.user and request.user.is_staff)

class TheatreHallViewSet(viewsets.ModelViewSet):
    queryset = TheatreHall.objects.all()
    serializer_class = TheatreHallSerializer
    permission_classes = [IsAdminOrReadOnly]

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]

class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = [IsAdminOrReadOnly]

class PlayViewSet(viewsets.ModelViewSet):
    queryset = Play.objects.prefetch_related("genres", "actors")
    serializer_class = PlaySerializer
    permission_classes = [IsAdminOrReadOnly]

class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.select_related("play", "theatre_hall")
    serializer_class = PerformanceSerializer
    permission_classes = [IsAdminOrReadOnly]

    @action(detail=True, methods=["get"])
    def seats(self, request, pk=None):
        performance = self.get_object()
        hall = performance.theatre_hall
        taken = list(performance.tickets.values_list("row", "seat"))
        return Response({
            "performance": performance.id,
            "hall": {"rows": hall.rows, "seats_in_row": hall.seats_in_row},
            "taken": [{"row": r, "seat": s} for r, s in taken],
        })

class ReservationViewSet(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    queryset = Reservation.objects.prefetch_related("tickets").select_related("user")
    serializer_class = ReservationSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset
        return self.queryset.filter(user=self.request.user)

    @action(detail=False, methods=["get"], url_path="my")
    def my(self, request):
        qs = self.get_queryset().order_by("-created_at")
        page = self.paginate_queryset(qs)
        ser = ReservationSerializer(page or qs, many=True)
        return self.get_paginated_response(ser.data) if page is not None else Response(ser.data)

    def create(self, request, *args, **kwargs):
        payload = CreateReservationSerializer(data=request.data)
        payload.is_valid(raise_exception=True)
        performance = payload.validated_data["performance"]
        seats = payload.validated_data["seats"]

        try:
            with transaction.atomic():
                reservation = Reservation.objects.create(user=request.user)
                for seat in seats:
                    Ticket.objects.create(
                        performance=performance,
                        reservation=reservation,
                        row=seat["row"],
                        seat=seat["seat"],
                    )
        except IntegrityError:
            return Response(
                {"detail": "Деякі з вибраних місць вже зайняті."},
                status=status.HTTP_409_CONFLICT,
            )

        return Response(ReservationSerializer(reservation).data, status=status.HTTP_201_CREATED)
