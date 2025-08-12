from django.conf import settings
from django.db import models
from django.db.models import Q

from theatre import settings


class TheatreHall(models.Model):
    name = models.CharField(max_length=100)
    rows = models.PositiveIntegerField()
    seats_in_row = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.rows}*{self.seats_in_row})"


class Genre(models.Model):
    name = models.CharField(
        max_length=64,
        unique=True
    )

    def __str__(self):
        return self.name


class Actor(models.Model):
    first_name = models.CharField(
        max_length=64
    )
    last_name = models.CharField(
        max_length=64
    )

    class Meta:
        unique_together = ("first_name", "last_name")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Play(models.Model):
    title = models.CharField(
        max_length=250
    )
    description = models.TextField(
        blank=True
    )
    genres = models.ManyToManyField(
        Genre,
        related_name="plays",
        blank=True
    )
    actors = models.ManyToManyField(
        Actor,
        related_name="plays",
        blank=True
    )
    def __str__(self):
        return self.title


class Performance(models.Model):
    play = models.ForeignKey(
        Play,
        on_delete=models.CASCADE,
        related_name="performances",
    )
    theatre_hall = models.ForeignKey(
        TheatreHall,
        on_delete=models.PROTECT,
        related_name="performances",
    )
    show_time = models.DateTimeField()

    class Meta:
        indexes = [models.Index(fields=["theatre_hall", "show_time"])]
        unique_together = ()

    def __str__(self):
        return f"{self.play.title} @ {self.theatre_hall} {self.show_time:%Y-%m-%d %H:%M}"


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reservations",
    )

    def __str__(self):
        return (
            f"Reservation {self.id} by {self.user} at {self.created_at:%Y-%m-%d %H:%M}"
        )


class Ticket(models.Model):
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()
    performance = models.ForeignKey(
        Performance,
        on_delete=models.CASCADE,
        related_name="tickets",
    )
    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.CASCADE,
        related_name="tickets",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["performance", "row", "seat"],
                name="unique_seat_per_performance",
            ),
            models.CheckConstraint(
                check=Q(row__gte=1) & Q(seat__gte=1),
                name="row_seat_ge_1"
            )
        ]

    def __str__(self):
        return f"{self.performance} - r{self.row}s{self.seat} "