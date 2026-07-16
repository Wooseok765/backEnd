from rest_framework.views import APIView
from rooms.models import Amenity, Room
from rooms.serializer import (
    AmenitySerializer,
    AmenitySerializerAll,
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
from reviews.serializer import ReviewSerializer
from medias.serializers import PhotoSerializer
from medias.models import Photo


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


class RoomReviews(APIView):
    def get_objects(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = request.query_params.get(
                "page", 1
            )  # http://127.0.0.1:8000/api/v1/rooms/1/reviews를 했을때 기본값 반환(page=1)
            # reverse serializer로는 모든 객체를 한 번에 반환하기 때문에 객체가 많아지면 비효율
            # pagination을 하기 위해 url에 들어있는 querty_parameter(중에서 page 속성)의 값을 가져오는것
            # Django에서 .../.../...?page= 식으로 pagination 할 수 있게 자동으로 설정되며 등호 뒤에 숫자로 페이지 설정가능
            # string type이 반환되기에 변환 필요
            page = int(
                page
            )  # page= 뒤에 숫자가 아닌값을 넣으면 오류발생함(기본값 불러오기도 안됨 그건 아무것도 안적거나 없는 '숫자'를 넣었을때 발동)
        except ValueError:  # page 1로 보내버림
            page = 1
        page_size = 3
        start = (page - 1) * page_size
        end = start + page_size
        room = self.get_objects(pk)
        reviews = room.reviews.all()[
            start:end
        ]  # query_parameter가 새로 들어올 때마다 화면에 해당하는 순번의 리뷰들을 표시(페이지를 구분했다는 뜻)
        # reviews = room.reviews.all()[0:3] # 첫 번째부터 세번째 리뷰만 받아오는것
        # reverse accessor
        serializer = ReviewSerializer(
            reviews,
            many=True,
        )
        return Response(serializer.data)


class RoomAmenity(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise ParseError("Room not found")

    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1
        page_size = 2
        start = (page - 1) * page_size
        end = start + page_size
        room = self.get_object(pk)
        amenities = room.amenity.all()[start:end]
        serializer = AmenitySerializerAll(
            amenities,
            many=True,
        )
        return Response(serializer.data)

class RoomPhotos(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise ParseError(f"room({pk}) not found")
        
    def post(self, request, pk): # 특정 room 객체에 넣을 사진이기 때문에 pk 필요
        room = self.get_object(pk)
        if not request.user.is_authenticated: # 사진 업로드하는 사람이 해당 Room 객체의 주인인지 확인하는 과정
            raise NotAuthenticated
        if request.user != room.owner:
            raise self.permission_denied
        serializer = PhotoSerializer(data=request.data) # 유저가 업로드하는 사진/영상을 받는것
        if serializer.is_valid():
            photo = serializer.save(rooms=room)
            # 검증된 데이터를 DB에 저장하는 단계
            # Photo 객체의 필드인 room(foreignkey type)의 값을 지정하는것(pk값으로 DB에서 가져온 객체)
            serializer = PhotoSerializer(photo)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)