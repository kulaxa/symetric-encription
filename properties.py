import redis

INIT_ADDRESS = "databaseinitaddress"
INIT_PASSWORD = "databaseinitpassword"

r = redis.Redis(
    host='localhost',
    port=6379,
    db=0)
