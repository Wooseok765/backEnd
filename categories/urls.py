from django.urls import path
from categories import views

urlpatterns = [
    path("", views.Categories.as_view()),
    # as_view()의 기능은 HTTP method에 따라서 자동으로 클래스 내부의 def를 선택하도록 함
    path("<int:pk>", views.CategoryDetail.as_view()),
]
