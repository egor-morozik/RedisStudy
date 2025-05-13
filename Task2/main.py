import redis
import json

RDB = redis.Redis(host='localhost', port=6379, decode_responses=True)

def add_task(task_data):
    task_json = json.dumps(task_data)
    RDB.rpush("task_queue", task_json)

def process_task():
    task = RDB.blpop("task_queue", timeout=5)
    if task:
        return json.loads(task[1])
    return None

add_task({"task_id": 1, "type": "send_email", "to": "user@example.com"})
add_task({"task_id": 2, "type": "send_email", "to": "user2@example.com"})

print(process_task())  
print(process_task())  
print(process_task())  