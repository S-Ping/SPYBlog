from celery import Celery

app = Celery('tasks', broker='redis://localhost:3306/6')

app.conf.CELERYD_CONCURRENCY = 4
CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24  # 任务过期时间


@app.task
def send_sms(*args, **kwargs):
    """发短信"""
    pass


@app.task
def send_mail(*args, **kwargs):
    """发邮件"""
    pass


