#========================================
# Scheduler Jobs
#========================================
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import utc
scheduler = BackgroundScheduler()
scheduler.configure(timezone=utc)

# jobs
from attikmoney.scheduler import scheduler_jobs

#scheduler.add_job(scheduler_jobs.OrdersRates, 'interval', seconds=1)
scheduler.add_job(scheduler_jobs.OrdersRates, trigger='cron', day_of_week='mon-fri', hour='18-20')
#scheduler.add_job(scheduler_jobs.OrdersRates, 'cron', hour='12-20')

scheduler.start()



#========================================