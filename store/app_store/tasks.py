from store.celery import app
from .service import send


@app.task
def send_payment(email):
    send(email)
