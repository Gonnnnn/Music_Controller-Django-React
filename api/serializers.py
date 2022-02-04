from rest_framework import serializers
from .models import Room

# serializer translates an object and its information(object members and such)
# into a Json response
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        # list all of the fields that we want to include in the output or serialization
        fields = (
            # each of our model has sth called primary key
            # and it's an unique integer
            "id",
            "code",
            "host",
            "guest_can_pause",
            "votes_to_skip",
            "created_at",
        )


# 다른 request나 response를 다룰 때, serializer을 각각 구현해주는게 좋다.
class CreateRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ("guest_can_pause", "votes_to_skip")
