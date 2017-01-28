from datetime import datetime, timedelta
from celery import Celery
 
app = Celery('page_saver')
app.conf.update(
    BROKER_URL='redis://localhost',
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],
    CELERYBEAT_SCHEDULE={
        'save_page':{
            'task':'print_current_time',
            'schedule': timedelta(minutes=1)
        }
    }
)
 
@app.task(name='print_current_time')
def print_current_time():
    print(datetime.now())