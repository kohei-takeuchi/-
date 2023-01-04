from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm,devicedata
from django.http import HttpResponse
from account.models import Account
import shutil
import sys
import json
import os
import time
from django.views.generic.edit import FormView
from web.models import depthdata
from .csvtogeojson import csv2geojson,datatopreview,datainput
from django.contrib.auth.decorators import login_required
# ------------------------------------------------------------------
@login_required
def file_upload(request):
    userid = request.user.uuid
    uploadtime=time.time()
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():           
            file_obj = request.FILES['file']
            file_path = 'media/documents/' + str(userid) + str(uploadtime) +'.csv'
            with open(file_path, 'wb+') as destination:
               for chunk in file_obj.chunks():
                   destination.write(chunk)
            return HttpResponseRedirect('/upload/preview/'+str(userid) +'/'+ str(uploadtime) +'.csv')
    else:
        form = UploadFileForm()
    return render(request, 'upload/index.html', {'form': form})
#
#
# ------------------------------------------------------------------  
def file_preview(request,username,csvname):
    t=datatopreview('media/documents/' + username+csvname)
    if request.method == 'POST':
        form = depthdata(request.POST)
        if "upload_button" in request.POST:
            device =  request.POST['device']
            depth =  request.POST['depth']
            point=handle_uploaded_file('media/documents/' + username+csvname,username,device,depth)
            context = {
               'getpoint': str(point),
            } 
            return render(request,'upload/success.html',context)
        if "cancel_button" in request.POST:
            os.remove('media/documents/' + username+csvname)
            return HttpResponseRedirect('/upload')                       
    context = {
           'form':devicedata(initial={'device':'deeper','depth':0.0}),
           'previewdata': json.dumps(t),
       }
    return render(request, 'upload/preview.html',context)
#
#------------------------------------------------------------------
def handle_uploaded_file(file_path,userid,device,depth):
    point=csv2geojson(file_path,userid,time.time(),device,depth)
    os.remove(file_path)
    return point
#  ------------------------------------------------------------------

