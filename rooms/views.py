from django.db import transaction
from django.utils import timezone
from rest_framework.views import APIView
from rooms.models import Amenity, Room
from rest_framework.response import Response
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rooms.serializer import (
    AmenitySerializer,
    AmenitySerializerAll,
    RoomSerializer,
    RoomListSerializer,
    RoomDetailSerializer,
)
from categories.models import Category
from reviews.serializer import ReviewSerializer
from medias.serializers import PhotoSerializer
from medias.models import Photo
from bookings.models import Booking
from bookings.serializer import PublicBookingSerializer

# HTTP request가 get인 경우 누구나 통과시킴, 나머지 요청의 경우 사용자 일치여부 진행


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
            return Response(
                serializer.errors
            )  # valid가 실패한 구체적인 오류내역(status= 구문이 생략된 형태(기본값으로 포함됨))


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
        return Response(
            status=HTTP_204_NO_CONTENT
        )  # 별다른 내용없이 시스템 코드만 반환하여 보여주는 형태


class Rooms(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Rooms API(현재 클래스를 말함)을 사용하는 url(ip/api/v1/rooms/)로 접근하는 경우
    # 접근자의 로그인여부를 확인하여 비로그인시 get handler에만 접근 허용, 로그인시 나머지도 승인
    def get(self, request):
        all_rooms = Room.objects.all()
        serilizer = RoomListSerializer(
            all_rooms,
            many=True,
            context={
                "request": request,
            },  # 현재 HTTP 요청 객체를 serializer 내부로 전달해서, serializer가 요청 정보에 접근할 수 있게 하는 것
        )
        return Response(serilizer.data)

    def post(self, request):

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


class RoomDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

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
    permission_classes = [IsAuthenticatedOrReadOnly]

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

    def post(self, request, pk):
        serializer = ReviewSerializer(data=request.data)
        # request.data를 ReviewSerializer의 쓰기 가능한 필드로 검증한다.
        # user는 read_only=True이므로 입력·검증 대상에서 제외되고,
        # 사용자가 직접 입력하는 값은 payload와 rating이다.
        if serializer.is_valid():
            review = serializer.save(
                user=request.user,
                room=self.get_objects(pk),
            )
            # 검증된 payload, rating에
            # 서버가 결정한 user와 room을 추가하여 Review 객체를 생성한다.(review 객체의 필드인 user, room을 서버에서 가져온다)
            # user = 로그인 한 사용자, room = 리뷰를 작성하고있는 방
            # user와 room은 Review 모델의 실제 필드명과 일치해야 한다.
            serializer = ReviewSerializer(review)
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

    def post(self, request, pk):  # 특정 room 객체에 넣을 사진이기 때문에 pk 필요
        room = self.get_object(pk)
        if (
            not request.user.is_authenticated
        ):  # 사진 업로드하는 사람이 로그인 된 사람인지 체크
            raise NotAuthenticated
        if (
            request.user != room.owner
        ):  # 사진 업로드 유저가 외부키로 합쳐질 room객체의 owner와 동일한지 체크
            raise self.permission_denied
        serializer = PhotoSerializer(
            data=request.data
        )  # 유저가 업로드하는 사진/영상을 받는것
        if serializer.is_valid():
            photo = serializer.save(rooms=room)
            # 검증된 데이터를 DB에 저장하는 단계
            # Photo 객체의 필드인 room(foreignkey type)의 값을 지정하는것(pk값으로 DB에서 가져온 객체)
            serializer = PhotoSerializer(photo)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class RoomBookings(APIView):
    # 특정 Room에 연결된 예약 목록 조회 및 예약 생성을 처리한다.
    # URL이 /rooms/<room_pk>/bookings 형태이고,
    # 요청의 기준이 Booking이 아니라 Room이므로 rooms 앱의 view에 둔다.

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise ParseError("room not found")

    def get(self, request, pk):
        room = self.get_object(pk)
        now = timezone.localtime(timezone.now()).date()
        # timezone.localtime(timezone.now()) 현지 시각 반환함. date()를 추가하면 시간은 생략된 날짜만 반환함
        bookings = Booking.objects.filter(
            room=room,
            kind=Booking.KindOfBookingChoice.ROOM,
            check_in__gt=now,
            # check_in의 값이 now의 값을 초과하는 조건을 충족하는 booking 객체를 반환하게함
        )
        # 선택필드인 kind의 값(클래스에서 선택된 값이 ROOM인 경우)
        # DB를 2번 조회하여 room객체 존재여부까지 검증
        """
        bookings = Booking.objects.filter(room__pk = pk)
        # 유저가 보낸 룸 id(pk)가 포함된 booking들을 전부 보냄
        # 유저가 보낸 id와 일치하는 room객체의 존재여부 검증안함, DB조회를 한 번만 한다는 의미, Relationship으로 filter할 때 자주 쓰이는 방법
        # 없을경우 empty queryset 반환함
        """
        serializer = PublicBookingSerializer(bookings, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        room = self.get_object(pk)
        serializer = PublicBookingSerializer(data=request.data)
        if serializer.is_valid():
            pass
        else:
            return Response(serializer.errors)
