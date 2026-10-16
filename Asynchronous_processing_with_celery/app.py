import time
from flask import Flask, jsonify, request
from celery import Celery

app=Flask(__name__)

# Celery Configuration: Redis serves as both broker and result backend

app.config['CELERY_BROKER_URL']='redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND']='redis://localhost:6379/0'

celery=Celery(
    app.import_name,
    broker=app.config['CELERY_BROKER_URL'],
    backend=app.config['CELERY_RESULT_BACKEND']
)

celery.conf.update(app.config)

# defining celery task
@celery.task(name='send_email_task')
def send_email_task(to_email):
    time.sleep(10) #Simulates slow I/0 operation (e.g SMTP transmission)
    return f"Email sent to {to_email}"


@app.route('/send-email',methods=['POST'])
def send_email():
    data=request.get_json()
    to_email=data.get('to')

    if not to_email:
        return jsonify({"error":"to field is required"}),400

    # Offload task to Celery queue
    task=send_email_task.delay(to_email)

    return jsonify({
        "message":"Email is being sent in the background",
        "task_id":task.id
    }), 202


@app.route('/task-status/<task_id>',methods=['GET'])
def task_status(task_id):
    task=send_email_task.AsyncResult(task_id)

    response={
        "task_id":task_id,
        "status":task.status,
    }

    if task.status=="SUCCESS":
        response["result"]=task.result

    return jsonify(response)

if __name__=='__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)