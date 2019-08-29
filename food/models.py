from django.db import models
from django.urls import reverse
from jsonfield import JSONField


class Category(models.Model):
    name = models.CharField(max_length=50, db_index=True)  # 카테고리 이름(종류별 이름)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('food:category_detail', args=[self.pk])


class Shop(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # 카테고리
    name = models.CharField(max_length=50)  # 가게 이름
    desc = models.TextField(blank=True)  # 설명
    latlng = models.CharField(max_length=100, blank=True)  # 좌표
    photo = models.ImageField(blank=True)  # 사진
    meta = JSONField()  # 나머지 필요한 내용들 meta로 저장

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('food:shop_detail', args=[self.pk])

    @property
    def address(self):
        return self.meta.get('address')
