import redis
from datetime import datetime

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def track_visitor(page, user_id):
    date = datetime.now().strftime("%Y-%m-%d")
    key = f"visitors:{page}:{date}"
    
    r.sadd(key, user_id)
    
    r.expire(key, 24 * 60 * 60)

def get_unique_visitors(page):
    date = datetime.now().strftime("%Y-%m-%d")
    key = f"visitors:{page}:{date}"
    return r.scard(key)

track_visitor("homepage", "user1")
track_visitor("homepage", "user2")
track_visitor("homepage", "user1")  
print(get_unique_visitors("homepage")) 