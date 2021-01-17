from django.urls import path
from .views import CreateRoomView, JoinRoom, RoomView, GetRoom

urlpatterns = [
    path('room', RoomView.as_view()),
    path('create_room', CreateRoomView().as_view()),
    path('get-room', GetRoom().as_view()),
    path('join-room', JoinRoom().as_view()),

]
