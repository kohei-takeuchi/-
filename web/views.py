from django.shortcuts import render
from web.models import depthdata,purchasedata,correctdata,lightdata
from account.models import Account
from django.contrib.auth.decorators import login_required
import numpy as np
from django.http import HttpResponseRedirect
from upload.csvtogeojson import csv2geojson,datatopreview,datainput
import time
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import *
from django.contrib.gis.measure import D
@login_required
def index_show(request):
    userid = request.user.uuid
    purchase=purchasedata.objects.filter(ID=userid)
    if purchase.count()==0:
        return render(request,'web/nopurchase.html')   
    else:
        for num in range(purchase.count()):
            if num==0:
                area=purchasedata.objects.get(lat=purchase[0].lat,lon=purchase[0].lon,ID="admin")
                data=lightdata.objects.filter(geom__within=area.geom)
            else:
                area=purchasedata.objects.get(lat=purchase[num].lat,lon=purchase[num].lon,ID="admin")
                data=data+lightdata.objects.filter(geom__within=area[num])
        context = {
            'data':data,
            'purchase': purchase,
        }
        return render(request,'web/index.html',context)
@login_required 
def correctdata_show(request,lat,lon):
    userid = request.user.uuid
    correct=correctdata.objects.filter(緯度=float(lat), 経度=float(lon))
    purchase=purchasedata.objects.filter(geom__covers=correct[0].geom)
    if purchase.count()==0:
        return render(request,'web/nopurchase.html')   
    else: 
        data=depthdata.objects.filter(geom__within=correct[0].geom).order_by('計測時刻')
        context = {
            'data':data,
        }
        return render(request,'web/correctdata.html',context)
@login_required 
def correct_show(request):
    userid = request.user.uuid
    purchase=purchasedata.objects.filter(ID=userid,rank=2)
    if purchase.count()==0:
        return render(request,'web/nopurchase.html')   
    else:
        for num in range(purchase.count()):
            if num==0:
                area=purchasedata.objects.get(lat=purchase[0].lat,lon=purchase[0].lon,ID="admin")
                data=correctdata.objects.filter(geom__within=area.geom)
            else:
                area=purchasedata.objects.get(lat=purchase[num].lat,lon=purchase[num].lon,ID="admin")
                data=data+correctdata.objects.filter(geom__within=area[num])
        context = {
            'data':data,
            'purchase': purchase,
        }
        return render(request,'web/correct.html',context)
        
@login_required 
def mydata_show(request):
    userid = request.user.uuid
    context = {
            'mydata':depthdata.objects.filter(投稿者=userid),
    }
    return render(request,'web/yourdata.html',context)  
@login_required 
def all_show(request):
    userid = request.user.uuid
    purchase=purchasedata.objects.filter(ID=userid)
    if purchase.count()==0:
        return HttpResponseRedirect('/web/mydata')   
    else: 
        for num in range(purchase.count()):
            if num==0:
                area=purchasedata.objects.get(lat=purchase[0].lat,lon=purchase[0].lon,ID="admin")
                data=depthdata.objects.filter(geom__within=area.geom)
            else:
                area=purchasedata.objects.get(lat=purchase[num].lat,lon=purchase[num].lon,ID="admin")
                data=data+depthdata.objects.filter(geom__within=area[num])
        context = {
            'data':data,
            'mydata':depthdata.objects.filter(投稿者=userid),
            'purchase': purchase,
        }
        return render(request,'web/all.html',context)
@login_required 
def purchase_show(request):
    userid = request.user.uuid
    purchase=purchasedata.objects.filter(ID=userid).order_by('lat','lon')
    is_data=purchasedata.objects.filter(ID="admin").order_by('lat','lon')
    context = {
               'is_data': is_data,
               'purchase': purchase,
            }    
    return render(request,'web/purchase.html' ,context)
@login_required
def purchase_select(request,latitude,longitude):
    userid = request.user.uuid
    USER = Account.objects.get(uuid=userid)
    purchase=purchasedata.objects.filter(lat=latitude,lon=longitude,ID=userid)
    purchase1=purchasedata.objects.filter(lat=latitude,lon=longitude,ID=userid,rank="2") 
    is_data=purchasedata.objects.filter(lat=latitude,lon=longitude,ID="admin")
    if is_data.count()!=0:
        GEOM=purchasedata.objects.get(lat=latitude,lon=longitude,ID="admin")
        usepoint=int(123.476544*np.cos(np.radians(float(latitude)+0.05))*(1+(depthdata.objects.filter(geom__within=GEOM.geom).count()-2000)/4000))
        if purchase.count()==0:    
            if USER.unused_point >=usepoint:
                if "get_button" in request.POST:
                    limittime=time.time()+2592000
                    is_get=get_area(latitude,longitude,userid,usepoint,limittime)
                    if is_get==True:
                      purch=purchasedata.objects.get(lat=latitude,lon=longitude,ID=userid)
                      context = {
                      'limit':str(purch.time),  
                      'point': str(int(USER.unused_point)),
                      'usepoint': str(usepoint),                 
                      'usedpoint': str(int(USER.unused_point)-usepoint)
                      }              
                      return render(request,'web/success.html',context)
                    else:
                       return render(request,'web/failed.html')                      
                if "cancel_button" in request.POST:             
                    return HttpResponseRedirect('/web/purchase')                  
                context = {
                   'limit':str(time.time()+2592000),  
                   'lat':str(latitude),
                   'lon':str(longitude),
                   'data': depthdata.objects.filter(geom__within=GEOM.geom),
                   'point': str(int(USER.unused_point)),
                   'usepoint': str(usepoint),                 
                   'usedpoint': str(int(USER.unused_point)-usepoint),
                } 
                return render(request,'web/select.html',context)
            else:    
                context = {
                   'lat':str(latitude),
                   'lon':str(longitude),
                   'usepoint': str(usepoint),  
                   'point': str(USER.unused_point),            
                   'data': depthdata.objects.filter(geom__within=GEOM.geom),
                   'purchase': purchase,
                }
                return render(request,'web/nopoint.html',context) 
        elif purchase.count()!=0 and purchase1.count()==0:
          if USER.unused_point >=usepoint:
                if "get_button" in request.POST:
                    is_get=get_correct(latitude,longitude,userid,usepoint)
                    if is_get==True:
                      context = {
                      'point': str(int(USER.unused_point)),
                      'usepoint': str(usepoint),                 
                      'usedpoint': str(int(USER.unused_point)-usepoint)
                      }              
                      return render(request,'web/success.html',context)
                    else:
                      return render(request,'web/failed.html')  
                if "extend_button" in request.POST:
                    is_ext=extend_area(latitude,longitude,userid,usepoint)
                    if is_ext==True:
                      purch=purchasedata.objects.get(lat=latitude,lon=longitude,ID=userid)
                      context = {
                      'point': str(int(USER.unused_point)),
                      'usepoint': str(usepoint),
                      'limit':str(purch.time),              
                      'usedpoint': str(int(USER.unused_point)-usepoint)
                      }              
                      return render(request,'web/successextend.html',context)
                    else:
                      return render(request,'web/failed.html')
                if "cancel_button" in request.POST:             
                    return HttpResponseRedirect('/web/purchase')                  
                context = {
                   'lat':str(latitude),
                   'lon':str(longitude),
                   'limit':str(purchase[0].time),
                   'time':str(time.time()),
                   'data': correctdata.objects.filter(geom__within=GEOM.geom),
                   'point': str(int(USER.unused_point)),
                   'usepoint': str(usepoint),                 
                   'usedpoint': str(int(USER.unused_point)-usepoint),
                } 
                return render(request,'web/select2.html',context)
          else:    
                context = {
                   'lat':str(latitude),
                   'lon':str(longitude),
                   'limit':str(purchase[0].time),
                   'usepoint': str(usepoint),  
                   'point': str(USER.unused_point),            
                   'data': correctdata.objects.filter(geom__within=GEOM.geom),           
                }
                return render(request,'web/nopoint.html',context)                
        else:
          if USER.unused_point >=usepoint:
                if "extend_button" in request.POST:
                    is_ext=extend_area(latitude,longitude,userid,usepoint)
                    if is_ext==True:
                      purch=purchasedata.objects.get(lat=latitude,lon=longitude,ID=userid)
                      context = {
                      'point': str(int(USER.unused_point)),
                      'usepoint': str(usepoint),
                      'limit':str(purch.time),              
                      'usedpoint': str(int(USER.unused_point)-usepoint)
                      }          
                      return render(request,'web/successextend.html',context)
                    else:
                      return render(request,'web/failed.html')                    
                if "cancel_button" in request.POST:             
                    return HttpResponseRedirect('/web/purchase')                  
                context = {
                   'lat':str(latitude),
                   'lon':str(longitude),
                   'limit':str(purchase[0].time),
                   'time':str(time.time()),
                   'data': correctdata.objects.filter(geom__within=GEOM.geom),
                   'point': str(int(USER.unused_point)),
                   'usepoint': str(usepoint),                 
                   'usedpoint': str(int(USER.unused_point)-usepoint),
                } 
                return render(request,'web/select3.html',context)
          else:    
                context = {
                   'lat':str(latitude),
                   'lon':str(longitude),
                   'limit':str(purchase[0].time),
                   'usepoint': str(usepoint),  
                   'point': str(USER.unused_point),            
                   'data': depthdata.objects.filter(geom__within=GEOM.geom),
                   'purchase': purchase,
                }
                return render(request,'web/nopoint3.html',context)
    else:     
        context = {
                   'lat':str(latitude),
                   'lon':str(longitude),
                }
        return render(request,'web/nodata.html',context)
def get_area(latitude,longitude,userid,usepoint,limittime):
    USER = Account.objects.get(uuid=userid)
    AREA = purchasedata.objects.create(lat=latitude,lon=longitude,ID=userid,rank="1",time=limittime)
    AREA.save()
    is_success=purchasedata.objects.filter(lat=latitude,lon=longitude,ID=userid,rank="1",time=limittime)
    if is_success.count()==0:
      return False
    else:
      USER.unused_point=USER.unused_point-usepoint
      USER.save()
      return True
def extend_area(latitude,longitude,userid,usepoint):
    USER = Account.objects.get(uuid=userid)
    AREA = purchasedata.objects.get(lat=latitude,lon=longitude,ID=userid)
    newlimit=AREA.time+2592000
    AREA.time=newlimit
    AREA.save()
    is_success=purchasedata.objects.filter(lat=latitude,lon=longitude,ID=userid,time=newlimit)
    if is_success.count()==0:
      return False
    else:
      USER.unused_point=USER.unused_point-usepoint
      USER.save()
      return True
def get_correct(latitude,longitude,userid,usepoint):
    USER = Account.objects.get(uuid=userid)
    AREA = purchasedata.objects.get(lat=latitude,lon=longitude,ID=userid)
    AREA.rank=2
    AREA.save()
    is_success=purchasedata.objects.filter(lat=latitude,lon=longitude,ID=userid,rank=2)
    if is_success.count()==0:
      return False
    else:
      USER.unused_point=USER.unused_point-usepoint
      USER.save()
      return True
    USER.unused_point=USER.unused_point-usepoint
    USER.save() 
    
