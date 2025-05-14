import redis
import time
import json
from datetime import datetime

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

STREAM_KEY = "app_logs"
GROUP_NAME = "log_consumers"
CONSUMER_NAME = "worker_1"

def setup_stream():
    try:
        r.xgroup_create(STREAM_KEY, GROUP_NAME, id="0", mkstream=True)
    except redis.exceptions.ResponseError as e:
        if "BUSYGROUP" not in str(e):
            raise
    print(f"Group {GROUP_NAME} created")

def add_log(user_id, action):
    log_data = {
        "user_id": user_id,
        "action": action,
        "timestamp": datetime.utcnow().isoformat()
    }
    message_id = r.xadd(STREAM_KEY, log_data)
    print(f"Add log: {log_data}, ID: {message_id}")
    return message_id

def process_logs():
    while True:
        messages = r.xreadgroup(
            GROUP_NAME,
            CONSUMER_NAME,
            {STREAM_KEY: ">"},  
            count=1,  
            block=5000  
        )
        
        if not messages:
            print("Wait new logs...")
            continue
        
        for stream, message_list in messages:
            for message_id, message_data in message_list:
                print(f"Run log: {message_data}, ID: {message_id}")
                
                time.sleep(1)
                
                r.xack(STREAM_KEY, GROUP_NAME, message_id)
                print(f"Log {message_id} confirmed")
        
        pending = r.xpending(STREAM_KEY, GROUP_NAME)
        if pending and pending["pending"] > 0:
            print(f"Exsists {pending['pending']} unconfirmed massages")

if __name__ == "__main__":
    setup_stream()
    
    add_log("user123", "login")
    add_log("user456", "purchase")
    add_log("user789", "logout")
    
    print("Run log ...")
    process_logs()