import redis

INIT_ADDRESS = "databaseinitaddress"
INIT_PASSWORD = "databaseinitpassword"
PASSWORD_DELIMITER = ":"
r = redis.Redis(
    host='localhost',
    port=6379,
    db=0)
