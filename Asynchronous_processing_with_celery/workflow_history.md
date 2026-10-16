# step-1 - environment initialization
```
sudo apt update -y
sudo fuser -k 6379/tcp || true
sudo fuser -k 5000/tcp || true
```
# step-2 - Dependancy Installation
```
pip install flask celery redis
```

# step-3 - Redis setup
```
sudo apt install -y redis-server
sudo systemctl start redis-server
redis-cli ping # output: pong
```

# step-4
creating the app.py, initiating api endpoints and celery.

# step-5 - starting app in terminal 1
python3 app.py

# step-6 - start celery worker
celery -A app.celery worker --loglevel=info

# step -7 
sending request to celery worker with:
```
curl -X POST http://127.0.0.1:5000/send-email \
  -H "Content-Type: application/json" \
  -d '{"to": "user@example.com"}'
```

# step-8, checking status:

```
curl http://127.0.0.1:5000/task-status/<TASK_ID>
```