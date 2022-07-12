from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor
from decouple import config

from base.sql.session import get_db
from base.sql.models import UserModel

# Static variable
jobstores = {
    'default': SQLAlchemyJobStore(url=config('DB_URL'))
}
executors = {
    'default': ThreadPoolExecutor(20),
}
job_defaults = {
    'max_instances': 3,
}
scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone="Asia/Tehran")

# Credit resetter
def credit_resetter():
    db_session = get_db().__next__()
    users = db_session.query(UserModel).all()

    for user in users:
        user.search_credit = 5
        db_session.commit()

scheduler.add_job(credit_resetter, "interval", minutes=2) # hours=24
scheduler.start()