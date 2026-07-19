from django.test import TestCase
from rest_framework.test import APITestCase
from . import models
from users.models import User

# Create your tests here.

"""
테스트 코드는 나머지 코드의 기능이 정상적으로 작동하는지 테스트 한다
여기서 작성된 코드는 Django에 의해 실제 코드, 객체, api를 호출하여 기능을 점검한다
그래도 어떤 기능을 어떻게 불러서 어떤 반응이 나오는게 정상인지 개발자가 직접 입력해야한다
나중에 코드 수정 후 테스트 시 이상여부 확인가능(해당 코드에 요구하는 기능이 변하지 않았다면 오류x, 필드 명 혹은 필드옵션 변할 시 테스트 코드도 변경할 필요 있음)
"""


class TestAmenities(APITestCase):
    """
    def test_two_plus_two(self):#test_라는 키워드가 있어여 APITestCase를 상속한 클래스에서 실행될 수 있음. 여기서 self는 APITestCase를 의미한다
       self.assertEqual(2+2, 5, "Wrong")
       # console에 python manage.py test 하면 지들이 테스트 메서드 찾아서 실행함
    """

    NAME = "Amenity Test"
    DESC = "Amenity Des"
    URL = "/api/v1/rooms/amenities/"

    def setUp(self):
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESC,
        )

    # 1. 테스트용 DB 생성 2. setUp() 실행 3. Amenity 테스트 데이터 생성 및 테스트 DB에 저장 4. test_all_amenities() 실행 5. 결과 검사 * 검사완료 후 DB 삭제

    def test_all_amenities(self):

        response = self.client.get(self.URL)
        # get/post/put/delete같은 것들을 API로 보낼 수 있게 해준다(시뮬레이션)
        # 테스트 코드→ self.client.get()→ Django URL 설정→ 해당 View의 get() 실행→ Response 반환→ response 변수에 저장
        # 브라우저 없이 가상의 HTTP request를 만들어 Django에 전달하고, URL에 연결된 View를 실행한 후 HTTP response를 반환받는 테스트용 APIClient 객체
        # setUp()으로 만들어진 DB에서 get() 적용
        data = (
            response.json()
        )  # http응답의 json문자열을 python 자료형으로 변환(list or dictionary)

        self.assertEqual(
            response.status_code,
            200,
            "status code is not 200",
        )  # client객체가 get과 url을 이용하여 api로부터 받아온 response가 정상코드를 가지고 있는지(정상적으로 작동하여 정상적인 응답을 받았는지) 체크하는것. 최소한 요청 URL을 찾음, 해당 View가 실행됨, 권한 검사 등을 통과함, View가 응답을 반환함, 처리 중 예외가 발생하지 않음은 확인되었음
        # 상태 코드가 200이면 해당 API가 요청을 받아 정상적으로 응답했다는 뜻입니다. 하지만 API가 올바른 데이터를 반환했다는 것까지 증명하려면 response.data도 검사해야 합니다.

        self.assertIsInstance(
            data,
            list,
        )
        # HTTP 응답의 JSON 본문을 Python 자료형으로 변환했을 때, Amenity 목록이 list 형태인지 검사한다.

        self.assertEqual(
            len(data),
            1,
        )
        # pk없이 전체요청에 대한 응답이었기에 list형태로 답변이 옴
        # len(data)가 반환하는것은 객체의 숫자
        self.assertEqual(
            data[0]["name"],
            self.NAME,
        )
        # data의 0번째 아이템의 "name"이 self.NAME과 같은지 검사
        self.assertEqual(
            data[0]["description"],
            self.DESC,
        )

    def test_create_amenity(self):
        new_amenity_name = "New Amenity"
        new_amenity_description = "New Description"
        # url을 통해 정해진 데이터를 post method로 넘겼을 경우 생성될 response를 테스트해 보는것(반환되는 객체의 형식, 내용, 상태오류 등등)

        response = self.client.post(  # 정상적으로 객체가 생성되는경우의 반응 테스트
            self.URL,
            data={
                "name": new_amenity_name,
                "description": new_amenity_description,
            },
        )
        # 해당 url과 연결된 API내부의 method(post)에서 사용된 serializer를 보고 필요한 field를 넘기면 됨
        # setUp()에서 만들어진 객체가 저장된곳과 동일한 테스트 DB에 새로운 객체가 저장됨. 테스트 종료 후 삭제

        data = response.json()
        # HTTP response인 response를 python에서 list 혹은 dictionary 형태로 사용 가능하게끔 전환하는것

        self.assertEqual(
            response.status_code,
            200,
            "Not 200 status code",
        )

        self.assertEqual(data["name"], new_amenity_name)
        self.assertEqual(data["description"], new_amenity_description)

        response = self.client.post(
            self.URL,
            data={"description": new_amenity_description},
        )  # 잘못된 입력인 경우를 테스트
        # view.py에서 예외상황 return에 status=를 설정하지 않으면 error가 발생하여 else구문의 000.errors를 실행해도 상태코드는 기본값인 200을 반환하는 좆같은 상황이 발생한다.
        """
        print(response) # 상태코드만 보임
        print(response.json()) # 반환된 응답을 list형태로 변환한 모습을 보여줌
        """
        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertIn("name", data)
        # data는 {"name": ["This field is required."]}라는 응답을 가짐
        # 서버가 정상적으로 거부를 하였고(상태코드), 메시지도 반환하였다는 의미가 됨
        # 에러메시지에 name이라는 키워드가 있을것이란걸 알고있기에 가능한 테스트


class TestAmenity(
    APITestCase
):  # 새로운 API(즉, 또 다른 URL)을 테스트할 때 클래스를 구분한다
    NAME = "Test Amenity"
    DESC = "Test Description"
    URL = "/api/v1/rooms/amenities/1"
    # setUp하면

    def setUp(self):
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESC,
        )

    def test_amenity_notFound(self):
        response = self.client.get("/api/v1/rooms/amenities/2/")
        # 없는 어매니티 검색하는경우 오류발생여부 테스트(try/except 구문)

        self.assertEqual(response.status_code, 404)
        # 404 not found 정상 반환(setUP 이후 DB에는 pk1인 객체 1개밖에 없음)

    def test_get_amenity(self):

        response = self.client.get("/api/v1/rooms/amenities/1/")
        data = response.json()
        self.assertEqual(
            response.status_code,
            200,
        )
        self.assertIsInstance(
            data,
            dict,
        )
        self.assertEqual(
            data["name"],
            self.NAME,
        )
        self.assertEqual(
            len(data),
            2,
        )
        # pk1 만 요청하였고 그에대한 응답은 dictionary로 왔음
        # lan(data)가 반환하는것은 해당 객체가 가지고있는 key의 숫자

    def test_put_amenity(self):
        pass

    def test_delete_amenity(self):
        response = self.client.delete("/api/v1/rooms/amenities/1/")

        self.assertEqual(response.status_code, 204)


class TestRooms(APITestCase):
    # IsAuthenticatedOrReadOnly이 적용된 클래스를 테스트 할 예정
    def setUp(self):
        user = User.objects.create(
            username="Test"
        )  # user model 필수요구사항인 username 설정

        user.set_password("123")  # user model 필요 요구사항인 비밀번호 설정
        user.save()  # test DB에 저장

    def test_create_room(self):

        response = self.client.post("/api/v1/rooms/")
        self.assertEqual(response.status_code, 403)
        # 403 means the server is actively refusing your request to access a webpage. [IsAuthenticatedOrReadOnly] is working
        # 로그인 안되어있으니 접근 못한다는 뜻

        self.client.login(
            username="Test",
            password="123",
        )  # username, password가 DB의 값과 일치하면 로그인시키는 메서드

        response = self.client.post("/api/v1/rooms/")
        self.assertEqual(response.status_code, 400)
        # 유저 객체 생성 후 로그인까지 시킨 다음 url로 접근함
        # 빈 데이터로 접근하였기에 Response(serializer.errors) 이 반환된 상태
