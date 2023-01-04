from django.contrib.gis.db import models
class bufferdata(models.Model):
    緯度 = models.FloatField()
    経度 = models.FloatField()
    深さ = models.FloatField()
    補正 = models.FloatField()
    投稿者=models.CharField(max_length=36)
    計測時刻 = models.FloatField()  
    計測機器 = models.CharField(max_length=32)
    投稿時刻 = models.FloatField()
class depthdata(models.Model):
    緯度 = models.FloatField()
    経度 = models.FloatField()
    深さ = models.FloatField()
    投稿者=models.CharField(max_length=36)
    計測時刻 = models.FloatField()  
    計測機器 = models.CharField(max_length=32)
    投稿時刻 = models.FloatField()
    geom = models.PointField(srid=4326)
class correctdata(models.Model):
    緯度 = models.FloatField()
    経度 = models.FloatField()
    深さ = models.FloatField()
    最終変更時刻 = models.FloatField()
    geom = models.PolygonField(srid=4326)
class lightdata(models.Model):
    緯度 = models.FloatField()
    経度 = models.FloatField()
    深さ = models.FloatField()
    geom = models.PointField(srid=4326)
class purchasedata(models.Model):
    lat = models.FloatField(unique=False,primary_key=False)
    lon = models.FloatField(unique=False,primary_key=False)
    rank = models.FloatField(unique=False,primary_key=False)
    ID = models.CharField(max_length=36,unique=False,primary_key=False)
    time= models.FloatField(unique=False,primary_key=False)
    geom = models.PolygonField(srid=4326,null=True)
