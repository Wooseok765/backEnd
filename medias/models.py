from django.db import models
from common.models import CommonModel

# Create your models here.


class Photo(CommonModel):
    file = models.URLField()
    # imageField혹은 fileField 타입으로 Django에 직접 외부자료를 업로드하게끔 하는것은 위험함(해킹 등)
    # 외부 호스팅 전문 서버에 파일을 업로드 시키고 Django에는 해당 파일에 접근 가능한 url을 제공하는것이 안전
    description = models.TextField()
    rooms = models.ForeignKey(
        "rooms.Room",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="photos",
    )
    experiences = models.ForeignKey(
        "experiences.Experience",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="photos",
    )

    def __str__(self):
        return "photo file"


class Video(CommonModel):
    file = models.URLField()
    experiences = models.OneToOneField(
        "experiences.Experience",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return "video file"
