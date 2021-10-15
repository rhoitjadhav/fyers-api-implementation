# Packages
import redis


class RedisDatabase:
    def __init__(
            self,
            host: str = "localhost",
            port: int = 6390,
            db: int = 0,
            password: str = None,
            decode_responses: bool = True
    ):
        self._host = host
        self._port = port
        self._db = db
        self._password = password

        self._redis_client = redis.StrictRedis(self._host, self._port, self._db, self._password,
                                               decode_responses=decode_responses)

    def set(self, name, value):
        self._redis_client.set(name, value)

    def get(self, name):
        return self._redis_client.get(name)

    def hset(self, name, key=None, value=None, mapping=None):
        if key:
            self._redis_client.hset(name, key, value)
        else:
            self._redis_client.hset(name, mapping=mapping)

    def hgetall(self, name):
        return self._redis_client.hgetall(name)

    def hget(self, name, key):
        return self._redis_client.hget(name, key)
