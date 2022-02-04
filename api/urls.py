from django.urls import path
from .views import RoomView, CreateRoomView, GetRoom, JoinRoom, UserInRoom, LeaveRoom

urlpatterns = [
    path("room", RoomView.as_view()),
    path("create-room", CreateRoomView.as_view()),
    # RoomView class has as_view() method cuz it inherits fro generics
    path("get-room", GetRoom.as_view()),
    path("join-room", JoinRoom.as_view()),
    path("user-in-room", UserInRoom.as_view()),
    path("leave-room", LeaveRoom.as_view()),
]
