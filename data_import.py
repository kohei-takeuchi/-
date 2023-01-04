import os
import sys
import django
from upload import load_depthdata,load_correctdata,load_lightdata,load_purchasedata

sys.path.append("upload")
os.environ.setdefault('DJANGO_SETTINGS_MODULE','composeexample.settings')
#django.setup()
def dodata_import():
  print('do data import')
  load_depthdata.run()
def docorrect_import():
  print('correct import')
  load_correctdata.run()
def dolight_import():
  print('light data import')
  load_lightdata.run()
def dopurchase_import():
  print('purchase data import')
  load_purchasedata.run()
