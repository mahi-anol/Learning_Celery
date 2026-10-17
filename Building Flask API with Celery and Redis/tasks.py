import time
from celery_app import celery

@celery.task
def send_email(recipient):
    time.sleep(5)
    return f"Email send to {recipient}"

@celery.task
def generate_pdf(document_id):
    time.sleep(8)
    return f"PDF generated for document {document_id}"


