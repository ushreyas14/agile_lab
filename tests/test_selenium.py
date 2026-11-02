import pytest
import threading
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app as flask_app

BASE_URL = "http://localhost:5001"

@pytest.fixture(scope="module")
def server():
    flask_app.config['TESTING'] = True
    thread = threading.Thread(target=lambda: flask_app.run(port=5001, use_reloader=False))
    thread.daemon = True
    thread.start()
    time.sleep(2)
    yield

@pytest.fixture(scope="module")
def driver(server):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    d = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    yield d
    d.quit()


def test_home_page_loads(driver):
    driver.get(BASE_URL)
    assert "Student Attendance" in driver.title
    heading = driver.find_element(By.TAG_NAME, "h1")
    assert "Student Attendance" in heading.text


def test_add_student_via_ui(driver):
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 10)

    input_field = wait.until(EC.presence_of_element_located((By.NAME, "name")))
    input_field.clear()
    input_field.send_keys("SeleniumStudent")

    submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_btn.click()

    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "student-item")))
    page_source = driver.page_source
    assert "SeleniumStudent" in page_source


def test_attendance_page_accessible(driver):
    driver.get(f"{BASE_URL}/attendance")
    assert driver.current_url.endswith("/attendance") or "attendance" in driver.current_url
    assert driver.find_element(By.TAG_NAME, "h1")
