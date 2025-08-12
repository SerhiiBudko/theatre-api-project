from rest_framework import serializers
from .models import TheatreHall, Genre, Actor, Play, Performance, Reservation, Ticket


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("id", "name")


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model= Actor
        fields = (
            "id",
            "first_name",
            "last_name",
        )


class TheatreHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheatreHall
        fields = (
            "id",
            "name",
            "rows",
            "seats_in_row",
        )


class PlaySerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    actors = ActorSerializer(many=True, read_only=True)

    class Meta:
        model = Play
        fields = (
            "id",
            "title",
            "description",
            "genres",
            "actors",
        )


class PerformanceSerializer(serializers.ModelSerializer):
    play = PlaySerializer(read_only=True)
    play_id = serializers.PrimaryKeyRelatedField(
        queryset=Play.objects.all(),
        source="plays",
        write_only=True,
    )
    theatre_hall = TheatreHallSerializer(read_only=True)
    theatre_hall_id = serializers.PrimaryKeyRelatedField(
        queryset=TheatreHall.objects.all(),
        source="theatre_hall",
        write_only=True,
    )

    class Meta:
        model = Performance
        fields = (
            "id",
            "play",
            "play_id",
            "theatre_hall",
            "theatre_hall_id",
            "show_time"
        )


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = (
            "id",
            "row",
            "seat"
        )


class ReservationSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=True)

    class Meta:
        model = Reservation
        fields = (
            "id",
            "created_at",
            "tickets"
        )


class CreateReservationSerializer(serializers.Serializer):
    performance_id = serializers.PrimaryKeyRelatedField(
        queryset=Performance.objects.select_related("theatre_hall"), source="performance"
    )
    seats = serializers.ListField(
        child=serializers.DictField(child=serializers.IntegerField(min_value=1)),
        allow_empty=False,
    )

    def validate(self, attrs):
        performance = attrs["performance"]
        hall = performance.theatre_hall
        normalized = []
        for item in attrs["seats"]:
            row = item.get("row")
            seat = item.get("seat")
            if row is None or seat is None:
                raise serializers.ValidationError("Кожен елемент має містити 'row' і 'seat'.")
            if row > hall.rows or seat > hall.seats_in_row:
                raise serializers.ValidationError(
                    f"Місце r{row}s{seat} виходить за межі залу ({hall.rows}x{hall.seats_in_row})."
                )
            normalized.append({"row": row, "seat": seat})
        attrs["seats"] = normalized
        return attrs
