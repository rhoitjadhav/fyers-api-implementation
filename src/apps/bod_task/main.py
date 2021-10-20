# Packages
from selenium import webdriver

# Modules
from utils.helper import Helper
from db.redis_database import RedisDatabase
from constants.server_url import ServerUrl


class BODTask:
    def __init__(self, redis_client: RedisDatabase, server_url: str):
        self._server_url = server_url
        self._redis_client = redis_client

    def redis_flush_db(self):
        self._redis_client.flush_db()
        print("Redis Flush Completed")

    def generate_auth_code(self):
        url = self._server_url + ServerUrl.ENDPOINT_GENERATE_AUTH_CODE
        driver = webdriver.Chrome()
        driver.get(url)
