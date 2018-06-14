from apscheduler.schedulers.blocking import BlockingScheduler
from fb_bot.parser.parser import fill_db


sched = BlockingScheduler()


@sched.scheduled_job('interval', hours=12)
def timed_job():
    fill_db()
    print("Flushing and filling the database")


sched.start()

# python3 ./manage.py shell_plus < clocked_db.py
