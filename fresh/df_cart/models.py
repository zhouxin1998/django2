from django.db import models

# Create your models here.

class CartInfo(models.Model):
    user = models.ForeignKey('login.UserInfo')
    goods = models.ForeignKey('df_goods.GoodsInfo')
    count = models.IntegerField()


