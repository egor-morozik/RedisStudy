import redis
import threading
import time

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def subscriber(channel):
    pubsub = r.pubsub()
    pubsub.subscribe(channel)
    print(f"Subscribe on {channel}")
    for message in pubsub.listen():
        if message["type"] == "message":
            print(f"Received: {message['data']}")

def publish_message(channel, message):
    r.publish(channel, message)

channel = "news"

threading.Thread(target=subscriber, args=(channel,), daemon=True).start()

time.sleep(1)

publish_message(channel, "news 1: Redis cool!")
time.sleep(1)
publish_message(channel, "news 2: Python too!")