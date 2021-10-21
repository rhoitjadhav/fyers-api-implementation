# Packages
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Modules
from db.redis_database import RedisDatabase
from constants.server_url import ServerUrl


class BODTask:
    def __init__(self, fyers_username, fyers_password, pan_id, redis_client: RedisDatabase, server_url: str):
        self._fyers_username = fyers_username
        self._fyers_password = fyers_password
        self._pan_id = pan_id
        self._server_url = server_url
        self._redis_client = redis_client

    def redis_flush_db(self):
        self._redis_client.flush_db()
        print("Redis Flush Completed")

    def generate_auth_code(self):
        url = self._server_url + ServerUrl.ENDPOINT_GENERATE_AUTH_CODE

        driver = webdriver.Chrome()
        driver.get(url)
        driver.find_element(by=By.ID, value='fyers_id').send_keys(self._fyers_username)
        driver.find_element(by=By.ID, value='password').send_keys(self._fyers_password)
        driver.find_element(by=By.ID, value='pancard').send_keys(self._pan_id)
        driver.find_element(by=By.XPATH, value="//button[@id='btn_id']").click()

        WebDriverWait(driver, 20).until((EC.url_changes(driver.current_url)))
        print("Auth Code Generation Completed")
