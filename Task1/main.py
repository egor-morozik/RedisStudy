import redis
import time

RDB = redis.Redis(host='localhost', port=6379, decode_responses=True)
DB_DATA = {"name": "Alex", 
           "email": "alex@example.com"}

def get_user_profile(user_id):
    name = RDB.get(f"user:{user_id}:name")
    email = RDB.get(f"user:{user_id}:email")
    
    if not (name and email):             
        RDB.setex(f"user:{user_id}:name", 60, DB_DATA["name"])
        RDB.setex(f"user:{user_id}:email", 60, DB_DATA["email"])
    
    return {"name": name, "email": email}

print(get_user_profile(1))  
time.sleep(1)
print(get_user_profile(1))  
time.sleep(61)
print(get_user_profile(1))  