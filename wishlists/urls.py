from django.urls import path
from .views import Wishlists, WishlistsDetail

urlpatterns = [
    path("", Wishlists.as_view()),
    path("<int:pk", WishlistsDetail.as_view())
]