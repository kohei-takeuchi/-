import numpy as np
import sys
import math
import os
import glob
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import *
from django.contrib.gis.measure import D
from account.models import Account
from web.models import depthdata,purchasedata,correctdata,lightdata,bufferdata
import time
import data_import
def fixpoint(lat,lon,depth,correct,time,device):
   is_data=depthdata.objects.filter(緯度=lat,経度=lon,深さ=depth+correct,計測時刻=time,計測機器=device)
   if is_data.count() !=0:
      return 0
   else:
      cord = Point(lon,lat,srid=4326)
      res =depthdata.objects.filter(geom__distance_lte=(cord, 0.01))
      #if res.count()>n:
        #将来的に外れ値除去の処理
      point=1+math.floor(9/(res.count()+1))
      if device =="sonar":
         point=point*4
      if device == "multisonar":
         point=point*8
      if device == "deeper":
         point=point*2   
      return point/100

def csv2geojson(filename,user,dotime,device,depth):
     csv_float=[list(map(float,line.rstrip().split(","))) for line in open(filename).readlines()]
     data = np.array(csv_float)
     USER = Account.objects.get(uuid=user)
     point=0
     count=0
     if device =="deeper":
       for row in data:
          if count==0:
            count=row[3]  
          if row[3] >=(count+20000) and row[0]!=0:
           gettime=round(row[3]/1000,3)
           BUF = bufferdata.objects.create(緯度=row[0] ,経度=row[1],深さ=row[2],補正=0,計測時刻=gettime,計測機器=device,投稿者=user,投稿時刻=dotime)
           BUF.save()
           point+=1
       return point
     else :
       for row in data:
        if row[0]!=0:
           BUF = bufferdata.objects.create(緯度=row[0] ,経度=row[1],深さ=row[2],補正=float(depth),計測時刻=row[3],計測機器=device,投稿者=user,投稿時刻=dotime)
           BUF.save()
           point+=1
       return point
def removecsv():
  for file in glob.glob('media/documents/*.csv'):
    os.remove(file)
def registdata():
  path_w = 'upload/data/do.geojson'
  s = '{\n"type": "FeatureCollection",\n"features": ['
  with open(path_w, mode='w') as f:
     f.write(s) 
  BUF=bufferdata.objects.all().order_by('id').distinct().values_list('緯度','経度','深さ','計測時刻')
  if BUF.count()!=0:
   for DATA in BUF:
         buf=bufferdata.objects.filter(緯度=DATA[0],経度=DATA[1],深さ=DATA[2],計測時刻=DATA[3]).order_by('id')
         USER = Account.objects.get(uuid=buf[0].投稿者)
         rank =1+(math.floor(USER.exp/2000)*0.1)
         point =fixpoint(buf[0].緯度,buf[0].経度,buf[0].深さ,buf[0].補正,buf[0].計測時刻,buf[0].計測機器)
         if point !=0:
          admin = purchasedata.objects.filter(lat=str(round(math.floor(buf[0].緯度*10)/10,1)),lon=str(round(math.floor(buf[0].経度*10)/10,1)),ID="admin")
          if admin.count() == 0:
             datainput("purchase",buf[0].緯度,buf[0].経度,"admin","0")
          USER.exp += 10
          USER.unused_point += point*rank
          USER.save() 
          t='\n{ "type": "Feature", "properties": { "緯度": ' +str(buf[0].緯度)+', "経度": ' +str(buf[0].経度)+',"深さ": ' +str(buf[0].深さ)+',"計測時刻": ' +str(buf[0].計測時刻)+',"計測機器": "'+str(buf[0].計測機器)+'","投稿者": "' + str(buf[0].投稿者) +'","投稿時刻": ' + str(buf[0].投稿時刻) +' }, "geometry": { "type": "Point", "coordinates": [ ' +str(buf[0].経度)+', ' +str(buf[0].緯度)+ ' ] } },'
          with open(path_w, mode='a') as f:
              f.write(t)
   u = ']\n}'
   with open(path_w, mode='r') as f:
        t1=f.read()
   t=t1.rstrip(',')+'\n'
   with open(path_w, mode='w') as f:
        f.write(t) 
   with open(path_w, mode='a') as f:
        f.write(u)
   f.close()
   bufferdata.objects.all().delete()
   if t1==s:
         return False
   else:
         data_import.dodata_import()
         return True
  else:
   bufferdata.objects.all().delete()
   return False

def datatopreview(filename):
    csv_float=[list(map(float,line.rstrip().split(","))) for line in open(filename).readlines()]
    previewdata = np.array(csv_float)
    count=0
    time=0
    t = ''
    for row in previewdata:
        if row[0] !=0:
            t = t+str(row[0])+','+str(row[1])+','+str(row[2])+'\n'
    return t
def datainput(mode,lat,lon,user,other):
  if mode=="purchase":
    la=round(math.floor(lat*10)/10,1)
    lo=round(math.floor(lon*10)/10,1)
    with open('upload/data/purchase.geojson', mode='w') as f:
        t = '{\n"type": "FeatureCollection",\n"features": [\n{ "type": "Feature", "properties": { "lat": ' +str(la)+', "lon": ' +str(lo)+',"rank": ' +other +',"ID": "'+user+'","time": '+str(time.time())+' }, "geometry": { "type": "Polygon", "coordinates": [[[' +str(lo) +', ' +str(la) +'],[' +str(lo) +',' +str(la+0.1) +'],[' +str(lo+0.1) +', ' +str(la+0.1) +'],[' +str(lo+0.1) +', ' +str(la) +'],[' +str(lo) +', ' +str(la) +']]] } }]\n}'
        f.write(t)
    f.close()
    data_import.dopurchase_import()
  elif mode=="correct":  
    o=0.000005*math.sqrt(3)
    a=0.00001
    with open('upload/data/correct.geojson', mode='w') as f:
        t = '{\n"type": "FeatureCollection",\n"features": [\n{ "type": "Feature", "properties": { "緯度": ' +str(lat)+', "経度": ' +str(lon)+',"深さ": ' +other+',"最終変更時刻": '+str(time.time())+' }, "geometry": { "type": "Polygon", "coordinates": [[[' +str(lon+o) +', ' +str(lat+a) +'],[' +str(lon+2*o) +',' +str(lat) +'],[' +str(lon+o) +', ' +str(lat-a) +'],[' +str(lon-o) +', ' +str(lat-a) +'],[' +str(lon-2*o) +', ' +str(lat) +'],[' +str(lon-o) +', ' +str(lat+a) +'],[' +str(lon+o) +', ' +str(lat+a) +']]] } }]\n}'
        f.write(t)
    f.close()
    if other== "-1":
       llat=round((math.floor(lat/(2*a)))*2*a,5)
       llon=round((math.floor(lon/(2*a)))*2*a,5)
       light=lightdata.objects.filter(緯度=llat,経度=llon)
       if light.count()==0:
           datainput("light",llat,llon,"","-1")
       llat1=round(llat+2*a,5)
       light=lightdata.objects.filter(緯度=llat1,経度=llon)
       if light.count()==0:
           datainput("light",llat1,llon,"","-1")
       llon1=round(llon+2*a,5)
       light=lightdata.objects.filter(緯度=llat,経度=llon1)
       if light.count()==0:
           datainput("light",llat,llon1,"","-1")
       light=lightdata.objects.filter(緯度=llat1,経度=llon1)
       if light.count()==0:
           datainput("light",llat1,llon1,"","-1")
    data_import.docorrect_import()
  elif mode=="light":
    with open('upload/data/light.geojson', mode='w') as f:
        t = '{\n"type": "FeatureCollection",\n"features": [\n{ "type": "Feature", "properties": { "緯度": ' +str(lat)+', "経度": ' +str(lon)+',"深さ": ' +other+' }, "geometry": { "type": "Point", "coordinates": [ ' +str(lon) +', ' +str(lat)+ ' ] } }]\n}'
        f.write(t)
    f.close()  
    data_import.dolight_import()

def dataupdate(dotime):
  gte=dotime-90000
  changed_data=depthdata.objects.filter(投稿時刻__gte=gte)
  o=0.000015*math.sqrt(3)
  a=0.00001
  r=0.00001*math.sqrt(3)
  for data in changed_data:
    clon=round((math.floor(data.経度/o))*o,10)
    clat=round(((math.floor(data.緯度/(2*a))*2+math.floor(data.経度/(o))%2)*a),10)
    cor=correctdata.objects.filter(緯度=clat,経度=clon)
    if cor.count()==0:
       datainput("correct",clat,clon,"","-1")
    clat1=round(clat+a+a,10)
    cor=correctdata.objects.filter(緯度=clat1,経度=clon)
    if cor.count()==0:
       datainput("correct",clat1,clon,"","-1")
    clat1=round(clat+a,10)
    clon1=round(clon+o,10)
    cor=correctdata.objects.filter(緯度=clat1,経度=clon1)
    if cor.count()==0:
       datainput("correct",clat1,clon1,"","-1")
  correctd=correctdata.objects.all()
  for correct in correctd:
    COR = correctdata.objects.get(緯度=correct.緯度,経度=correct.経度)
    unloaddata=depthdata.objects.filter(geom__within=correct.geom)
    k=0
    d=0
    for unupload in unloaddata:
      k1=r-math.sqrt((unupload.緯度-correct.緯度)**2+(unupload.経度-correct.経度)**2)
      k=k+k1
      d=d+unupload.深さ*k1
    if k !=0:
      truedepth=round((d/k),3)
      COR.深さ=truedepth
      COR.最終変更時刻=dotime
      COR.save()   
  lightd=lightdata.objects.all()
  for light in lightd:
    LIG = lightdata.objects.get(緯度=light.緯度,経度=light.経度)
    undiv=correctdata.objects.filter(geom__distance_lte=(light.geom, a*2))
    k=0
    d=0
    for undi in undiv:
      if undi.深さ !=-1:
       k1=r-math.sqrt((undi.緯度-light.緯度)**2+(undi.経度-light.経度)**2)
       k=k+k1
       d=d+undi.深さ*k1
    if k !=0:
      truedepth=round((d/k),3)
      LIG.深さ=truedepth
      LIG.最終変更時刻=dotime
      LIG.save()
def erasepurchase(now):
   purchasedata.objects.filter(time__lte=now).exclude(ID="admin").delete()
def fixexp(pk,point):
 DEPTH=depthdata.objects.filter(id=pk)
 if DEPTH.count()==0:
   return False
 else:
   DEPTH=depthdata.objects.get(id=pk)
   USER = Account.objects.get(uuid=DEPTH.投稿者)
   USER.exp=USER.exp+point
   USER.save()
   return True
