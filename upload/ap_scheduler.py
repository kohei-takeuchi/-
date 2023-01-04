from datetime import datetime, date
from apscheduler.schedulers.background import BackgroundScheduler
import time
from web.models import *
from .csvtogeojson import *
def periodic_execution():
  registdata()
  now=time.time()
  dataupdate(now-90000)
  removecsv()

def start():
  scheduler = BackgroundScheduler()
  scheduler.add_job(periodic_execution, 'cron', hour=0, minute=0)
  scheduler.start()
