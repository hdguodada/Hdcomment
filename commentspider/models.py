from django.db import models

# Create your models here.


class WhereFrom(models.Model):
    name = models.CharField(max_length=20, verbose_name='评论网站')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '评论网站'
        verbose_name_plural = verbose_name


class HotelIndex(models.Model):
    """
    酒店信息,包含酒店名,酒店的所在网站的id,酒店所在网站的url,酒店所在网站的封面图url和封面图本地存储地址
    """
    hotel_name = models.CharField(max_length=50)
    hotel_id = models.IntegerField()
    hotel_url = models.URLField()
    hotel_front_img_url = models.URLField()
    hotel_front_img_path = models.ImageField()
    wherefrom = models.ForeignKey(WhereFrom, null=True, blank=True)

    class Meta:
        verbose_name = '酒店首页信息'
        verbose_name_plural = verbose_name


class HotelDetail(models.Model):
    guest_nickname = models.CharField(max_length=100, null=True, blank=True)
    guest_content = models.TextField(null=True, blank=True)
    create_time = models.DateTimeField(null=True, blank=True)
    commentExt_roomNum = models.CharField(max_length=20, null=True, blank=True)
    commentExt_roomTypeId = models.IntegerField(null=True, blank=True)
    commentExt_roomTypeName = models.CharField(max_length=20, null=True, blank=True)
    commentExt_checkInTime = models.DateTimeField(null=True, blank=True)
    replys_replyId = models.IntegerField(null=True, blank=True)
    replys_content = models.TextField(null=True, blank=True)
    replys_createTime = models.DateTimeField(null=True, blank=True)
    hotel = models.ForeignKey(HotelIndex, null=True, blank=True)
    wherefrom = models.ForeignKey(WhereFrom, null=True, blank=True)


class Reply_Image(models.Model):
    guest = models.ForeignKey(HotelDetail ,null=True, blank=True)
    guset_image = models.ImageField(null=True, blank=True)
