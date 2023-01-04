from datetime import datetime, date
from apscheduler.schedulers.background import BackgroundScheduler
import time
from upload.csvtogeojson import *

def periodic_execution():
  now=time.time()
  erasepurchase(now)
def start():
  scheduler = BackgroundScheduler()
  scheduler.add_job(periodic_execution, 'cron', hour=0, minute=0)
  scheduler.start()
