# step -1 - installing celery with redis support
```
pip install flask "celery[redis]"
docker run -d --name redis-broker -p 6379:6379 redis:7-alpine
redis-cli ping #expected: pong
```
# step - 2 creating files
cd 'Building Flask API with Celery and Redis'
touch app/__init__.py app/celery_app.py app/tasks.py app/main.py

# step - 3 - implementation

# step -4 - starting celery
celery -A celery_app.celery worker --loglevel=info

# step 5- run flask app
python -m flask --app main run --host 0.0.0.0 --port 5001

# step 6, checks
```
curl -X POST http://localhost:5001/send-email \
  -H "Content-Type: application/json" \
  -d '{"recipient": "user@example.com"}'


curl http://localhost:5001/status/<TASK_ID>
```

# step 7, cleaning environment
```
docker stop redis-broker

```