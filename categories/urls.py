from django.urls import path
from categories import views

urlpatterns = [
    path(
        "",
        views.CategoryViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
    ),
    path(
        "<int:pk>", #viewSet은 pk를 받도록 이미 작성되어있다"pk"라는 이름을 꼭 사용해야함
        views.CategoryViewSet.as_view(
            {
                "get": "retrieve",
                "put": "partial_update",
                "delete": "destroy",
            }
            # as_view({...})는 HTTP method를 ViewSet action에 연결한다.
            # 예: GET -> list, POST -> create
        ),
    ),
]
