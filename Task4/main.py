import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def save_user_settings(user_id, settings):
    key = f"user:{user_id}:settings"
    r.hset(key, mapping=settings)

def get_user_settings(user_id):
    key = f"user:{user_id}:settings"
    return r.hgetall(key)

def update_user_setting(user_id, field, value):
    key = f"user:{user_id}:settings"
    r.hset(key, field, value)

save_user_settings(1, {"language": "ru", "theme": "dark"})
print(get_user_settings(1))  
update_user_setting(1, "theme", "light")
print(get_user_settings(1))  