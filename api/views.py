from django.shortcuts import render

# it creates a class that inherits from a generic API view
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Room
from .serializers import RoomSerializer, CreateRoomSerializer
from django.http import JsonResponse

# Create your views here.

# it allows us to view all of the different rooms and create a rim
# so basically, this is a view that's already set up to return to us all of the different rooms
# generics.ListAPIView를 상속했을 때, 다른 view를 보여준다. 공식 doc을 읽고 익히자
class RoomView(generics.ListCreateAPIView):
    # all we  gotta give to this view are the followings

    # queryset is what we want to return
    queryset = Room.objects.all()
    # and the serializer class will convert it to JSON
    serializer_class = RoomSerializer


class GetRoom(APIView):
    serializer_class = RoomSerializer
    # code라는 방의 고유 code로 방을 구분할 것이기에 미리 이렇게 지정해주었다. 그냥 변수 선언이ㅏ.
    lookup_url_kwarg = "code"

    def get(self, request, format=None):
        # 단순히 server에 이러한 정보가 있는지 확인해 주는 것을 요청하는 것이므로 GET 방식 사용
        # request에서 GET.get을 통해 GET 방식으로 넘어온 request의 특정 인자를 가져올 수 있는 것 같다.
        code = request.GET.get(self.lookup_url_kwarg)
        # code가 넘어왔다면
        if code != None:
            # 먼저 그 방의 data 객체를 받아온다.
            room = Room.objects.filter(code=code)
            # room은 list로 받아와진다. 그런 room이 하나라도 존재한다면 (당연히 존재한다면 하나이겠지만 말이다)
            if len(room) > 0:
                # room serializer을 통해 room의 data를 얻어온다.
                data = RoomSerializer(room[0]).data
                # session_key를 통해 현재 request를 보낸쪽이 host인지 판단한다.
                # is_host를 추가한다. dictionary라서 단순히 아래와 같이 추가가 가능하다.
                data["is_host"] = self.request.session.session_key == room[0].host
                return Response(data, status=status.HTTP_200_OK)
            return Response(
                {"Room Not Found": "Invalid Room Code."},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            {"Bad Request": "Code paramater not found in request"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class JoinRoom(APIView):
    lookup_url_kwarg = "code"

    def post(self, request, format=None):
        # server측에 이러한 사람이 room에 join한다는 것을 알리고 무언가를 수정하기를 기대하므로 POST 방식
        # 막상 보니 뭐 바꾸거나 하지는 않는다. 더 잘 알아보자. 언제 post, 언제 get이 적절한지
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        # post request에서 data를 얻어올 때는 그냥 request.data.get()
        code = request.data.get(self.lookup_url_kwarg)
        if code != None:
            room_result = Room.objects.filter(code=code)
            if len(room_result) > 0:
                room = room_result[0]
                # session에 room_code라는 temporary storage object을 추가해줌으로써 user가 다시 돌아왔을 때
                # session이 종료되어있지 않았다면 다시 이 방으로 넣어주도록 하기 위해 아래와 같은 코드를 삽입
                # 이러한 방식으로 특정 정보를 user의 session에 추가할 수 있다.
                self.request.session["room_code"] = code
                return Response({"message": "Room Joined!"}, status=status.HTTP_200_OK)

            return Response(
                {"Bad Request": "Invalid Room Code"}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"Bad Request": "Invalid post data, did not find a code key"},
            status=status.HTTP_400_BAD_REQUEST,
        )


# APIView를 상속함으로써 get, post, put method등을 사용할 수 있다.
class CreateRoomView(APIView):
    serializer_class = CreateRoomSerializer

    def post(self, request, format=None):
        # session은 두 장치 사이의 일시적인 연결정도로 보면 된다.
        # session은 unique key를 갖고, 이를 통해 누가 누구인지 구분 가능한 것!
        # session이 유지된다면 굳이 계속해서 sign in 시킬 필요가 없을 것이다!
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        # request로 받아온 data들을 serialize 해서 python이 해독 가능하게 만들어준다.
        serializer = self.serializer_class(data=request.data)
        # 우리가 받고자 했던 request ("guest_can_pause", "votes_to_skip")가 유효한지 확인
        if serializer.is_valid():
            guest_can_pause = serializer.data.get("guest_can_pause")
            votes_to_skip = serializer.data.get("votes_to_skip")
            host = self.request.session.session_key
            # 먼저 Room.objects.filter로 해당 session key를 갖는 host가 있는지 찾아본다.
            queryset = Room.objects.filter(host=host)
            # 있다면
            if queryset.exists():
                room = queryset[0]
                # 만약 host가 이미 방이 있는데 또 만드려고 한다면, 기존의 방에 새로운 setting을 update해주는 식으로 해도 충분할 것
                room.guest_can_pause = guest_can_pause
                room.votes_to_skip = votes_to_skip
                # 새로 create하는게 아니라 update하는 것이므로 update_fields를 넘겨주고
                # list안의 것들을 강제로 update한다라는 것을 명시해주는 것이라고 한다.
                room.save(update_fields=["guest_can_pause", "votes_to_skip"])
                # room을 만들었으니, 이 session으로 들어오면 이 room으로 들어오도록 하게 하기 위해 Session에 code를 저장
                self.request.session["room_code"] = room.code
                # RoomSerializer은 해당 room을 인자로 받아 JSON 포맷으로 바꿔준다. 그 내용이 바로 data
                # status를 통해 request, response가 유효한지, 잘 처리되었는지를 나타낼 수 있다.
                return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)
            # 없다면
            else:
                # 새로 생성
                room = Room(
                    host=host,
                    guest_can_pause=guest_can_pause,
                    votes_to_skip=votes_to_skip,
                )
                room.save()
                # room을 만들었으니, 이 session으로 들어오면 이 room으로 들어오도록 하게 하기 위해 Session에 code를 저장
                self.request.session["room_code"] = room.code
                return Response(
                    RoomSerializer(room).data, status=status.HTTP_201_CREATED
                )

        return Response(
            {"Bad Request": "Invalid data..."}, status=status.HTTP_400_BAD_REQUEST
        )


class UserInRoom(APIView):
    def get(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        data = {"code": self.request.session.get("room_code")}
        # 자체적으로 만들어준 roomSerializer과 같은 역할을 한다. data를 JSON 형식으로 만들어서 보내주는 것
        # 다만 이 친구는 내가 생성한 model 객체가 아닌 dictionary형태로 데이터를 받아 전송해준다.
        return JsonResponse(data, status=status.HTTP_200_OK)


class LeaveRoom(APIView):
    # session에 있는 room code를 지우는 것도 하지만, host가 방을 나가면 room을 지워야 하기에
    # sever의 데이터를 건드려야한다. 다라서 post
    def post(self, request, format=None):
        if "room_code" in self.request.session:
            self.request.session.pop("room_code")
            user_id = self.request.session.session_key
            room_results = Room.objects.filter(host=user_id)
            if len(room_results) > 0:
                room = room_results[0]
                room.delete()

        return Response({"Message": "Success"}, status=status.HTTP_200_OK)
