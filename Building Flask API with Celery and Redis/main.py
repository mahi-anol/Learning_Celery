from flask import Flask, jsonify, request
from tasks import send_email
from celery_app import celery

app=Flask(__name__)

@app.route("/send-email",methods=["POST"])
def trigger_email():
    recipient = request.json.get("recipient")
    task=send_email.delay(recipient)
    return jsonify({"task_id":task.id}),202

@app.route("/status/<task_id>",methods=["GET"])
def check_status(task_id):
    result=celery.AsyncResult(task_id)
    return jsonify(
        {
            "task_id":task_id,
            "state":result.state,
            "result":result.result if result.ready() else None
        }
    )

if __name__=="__main__":
    app.run(host="0.0.0.0",port=5001)

