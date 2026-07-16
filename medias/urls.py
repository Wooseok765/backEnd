from django.urls import path
from .views import PhotoDetail

urlpatterns = [
    path("photos/<int:pk>/", PhotoDetail.as_view())
    # PhotoDetail을 직접 import했기때문에 다른 어플리케이션의 url.py에서처럼 views 불필요
]