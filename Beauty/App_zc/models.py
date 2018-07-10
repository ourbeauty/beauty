
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Address(models.Model):
    use = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    u_tel = models.CharField(max_length=11)
    u_provinces = models.CharField(max_length=1024)
    u_city = models.CharField(max_length=1024)
    u_county = models.CharField(max_length=1024)
    u_street = models.CharField(max_length=1024)
    u_email = models.CharField(max_length=1024)
    u_detailaddr = models.CharField(max_length=4096)
    u_addrstatus = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'address'


class Admin(models.Model):
    a_account = models.CharField(max_length=50)
    a_pwd = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'admin'


class Cart(models.Model):
    u = models.ForeignKey('User', models.DO_NOTHING)
    g = models.ForeignKey('Goods', models.DO_NOTHING)
    g_num = models.IntegerField()
    is_select = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'cart'


class GCategory(models.Model):
    c_name = models.CharField(max_length=50, blank=True, null=True)
    c_code = models.IntegerField(blank=True, null=True)
    c_desc = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'g_category'


class GCategory2(models.Model):
    c2_name = models.CharField(max_length=50, blank=True, null=True)
    c2_desc = models.CharField(max_length=255, blank=True, null=True)
    c2_code = models.IntegerField(blank=True, null=True)
    c_code = models.ForeignKey(GCategory, models.DO_NOTHING, db_column='c_code')

    class Meta:
        managed = False
        db_table = 'g_category2'


class Goods(models.Model):
    c_code = models.IntegerField()
    c2_code = models.IntegerField()
    g_name = models.CharField(max_length=50)
    g_desc = models.CharField(max_length=255, blank=True, null=True)
    g_info = models.CharField(max_length=255, blank=True, null=True)
    g_mktprice = models.CharField(max_length=20)
    g_price = models.CharField(max_length=20)
    g_goodsprops = models.CharField(max_length=255, blank=True, null=True)
    g_pics = models.CharField(max_length=255, blank=True, null=True)
    g_inventory = models.IntegerField()
    g_sale = models.IntegerField()
    g_status = models.IntegerField()
    g_createtime = models.DateTimeField(blank=True, null=True)
    g_changetime = models.DateTimeField(blank=True, null=True)
    g_class = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'goods'


class Goodsorder(models.Model):
    ord = models.ForeignKey('Orders', models.DO_NOTHING)
    g = models.ForeignKey(Goods, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'goodsorder'


class Orders(models.Model):
    # 关联用户
    u = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    # 价格
    o_price = models.FloatField()
    # 订单状态
    o_status = models.IntegerField()
    # 创建时间
    o_creattime = models.DateTimeField()
    # 修改时间
    o_changetime = models.DateTimeField()
    # 商品数量
    o_num = models.IntegerField()
    o_goods = models.ManyToManyField(Goods, through='Goodsorder')

    class Meta:
        managed = False
        db_table = 'orders'


class User(models.Model):
    # 用户名称
    u_name = models.CharField(max_length=1024)
    # 用户密码
    u_pwd = models.CharField(max_length=1024)
    # 电话
    u_tel = models.IntegerField(blank=True, null=True)
    # cookie
    u_ticket = models.TextField()
    # 过期时间
    u_outtime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user'
