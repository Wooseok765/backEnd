from rest_framework.views import APIView
from rooms.models import Amenity, Room
from rooms.serializer import (
    AmenitySerializer,
    RoomSerializer,
    RoomListSerializer,
    RoomDetailSerializer,
)
from rest_framework.response import Response
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from rest_framework.status import HTTP_204_NO_CONTENT
from categories.models import Category
from django.db import transaction


class Amenities(APIView):
    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(
            all_amenities, many=True
        )  # 아직 serialize 안된 model object를 반환
        return Response(serializer.data)

    def post(self, request):
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
            amenity = serializer.save()  # 아직 serialize 안된 model object를 반환
            return Response(AmenitySerializer(amenity).data)
        else:
            return Response(serializer.errors)


class AmenityDetail(APIView):
    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound()

    def get(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity)
        return Response(
            serializer.data,
        )

    def put(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(
            amenity,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated = serializer.save()
            return Response(
                AmenitySerializer(updated).data,
            )
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Rooms(APIView):
    def get(self, request):
        all_rooms = Room.objects.all()
        serilizer = RoomListSerializer(
            all_rooms,
            many=True,
            context={
                "request": request,
            },
        )
        return Response(serilizer.data)

    def post(self, request):
        if request.user.is_authenticated:
            serializer = RoomDetailSerializer(data=request.data)
            if serializer.is_valid():
                category_pk = request.data.get("category")
                if not category_pk:
                    raise ParseError("Category is required.")
                try:
                    categoryObj = Category.objects.get(pk=category_pk)
                    if categoryObj.kind == Category.KindChoice.EXPERIENCES:
                        raise ParseError("The category kind should be 'rooms'")

                except Category.DoesNotExist:
                    raise ParseError("Category not found")
                try:
                    with transaction.atomic():
                        # transaction 모듈의 아토믹 클래스
                        # Django가 with 내부의 코드들을 검수하며 임시저장함
                        # 오류 없을 시 적용, 오류 발생 시 임시저장파일 삭제
                        # 생성 후 삭제하는것 보다 효율적(id 누적문제 등)
                        room = serializer.save(
                            owner=request.user,
                            category=categoryObj,
                        )

                        amenity_list = request.data.get(
                            "amenity"
                        )  # It means the numbers user entered as a list form
                        for amenityItem in amenity_list:
                            amenity = Amenity.objects.get(pk=amenityItem)
                            room.amenity.set(amenity)

                        # room.amenity DB table에 행 추가(room id랑 amenity id로 이루어진 DB)
                        # 양 객체 모두 다른 객체 여러개와 연결될 수 있기에 추가적인 테이블에서 관리(각자의 DB table에 해당항목 표시 안함)
                        # .save()하면서 부여받은 roon pk를 기준으로 amenity id를 열에 배치함
                        serializer = RoomDetailSerializer(room)
                        return Response(serializer.data)
                except Exception:
                    raise ParseError("Amenity not found")
                    # with 구문 내에서 오류발생했다는것을 알려 줌
                    # 어떤 코드가 오류발생할 수 있는 것인지는 작성자가 판단해야함
            else:
                return Response(serializer.errors)
        else:
            raise NotAuthenticated


class RoomDetail(APIView):

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(room, context={"request": request})
        # Serializer class에 request 데이터를 "request"라는 이름으로 보내는 것
        # 해당 클래스 내부에서 self.context["request"]로 접근 가능하게된다
        return Response(serializer.data)

    def put(self, request, pk):
        room = self.get_object(pk)
        if not request.user.is_authenticated:
            raise NotAuthenticated

        if room.owner != request.user:
            raise PermissionDenied(
                f"{request.user} is not an owner. {room.owner} is authentic owner"
            )

        serializer = RoomDetailSerializer(
            room,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            categoryObj = room.category
            if "category" in request.data:
                category_pk = request.data.get("category")

                if not isinstance(category_pk, int):
                    raise ParseError(
                        "Category must be an integer ID.",
                    )

                try:
                    categoryObj = Category.objects.get(pk=category_pk)
                    # 유저가 카테고리 입력을 생략할 경우 pk=None이 될 수 있음
                    if categoryObj.kind == Category.KindChoice.EXPERIENCES:
                        raise ParseError("The category kind should be 'rooms'")
                except Category.DoesNotExist:
                    raise ParseError("Category not found")

            roomObj = serializer.save(owner=request.user, category=categoryObj)

            if "amenity" in request.data:
                amenity_list = request.data.get(
                    "amenity"
                )  # It means the numbers user entered as a list form

                amenities = []

                for amenityItem in amenity_list:
                    try:
                        amenity = Amenity.objects.get(pk=amenityItem)
                        amenities.append(amenity)
                    except Amenity.DoesNotExist:
                        raise ParseError(f"Amenity with id: {amenityItem} not found")

                roomObj.amenity.set(amenities)

            return Response(RoomDetailSerializer(roomObj).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        room = self.get_object(pk)
        if not request.user.is_authenticated:
            raise NotAuthenticated
        if room.owner != request.user:
            raise PermissionDenied
        room.delete()
        return Response(status=HTTP_204_NO_CONTENT)
