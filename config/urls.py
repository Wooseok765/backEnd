"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/rooms/", include("rooms.urls")),
    path("api/v1/categories/", include("categories.urls")),
    path("api/v1/experiences/", include("experiences.urls")),
    path("api/v1/medias/", include("medias.urls")),
    path("api/v1/wishlists/", include("wishlists.urls")),
    path("api/v1/users/", include("users.urls")),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# + static() :# /user_uploads/ 뒤에 오는 경로를 받아서 MEDIA_ROOT 안에서 같은 상대 경로의 파일을 찾아 반환한다.
# 사진을(resource마다 url이 필요한데) 올릴때마다 path를 추가하지 않기위해 포괄적인 규칙의 url을 요청시마다 생성하여 실행함

# media 파일에 접근할 시 http://127.0.0.1:8000/user_uploads/사진이름.확장자 식으로 url을 사용한다(urlpatterns와는 관계없는 url을 사용)
# settings.MEDIA_URL로 시작하는 url(user_uploads/사진파일이름.jpg)를 요청하면,
# 두 번째 argument에서(사진이 저장된 C:/.../.../uploads) 파일을 찾아서 반환

