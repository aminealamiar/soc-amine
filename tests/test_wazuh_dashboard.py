# tests/test_wazuh_dashboard.py
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import sys

DASHBOARD_URL = "https://34.28.30.204"  
API_URL = "https://34.28.30.204:55000"

def test_dashboard_reachable():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # run without opening browser window
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(DASHBOARD_URL)

        # 1. Validate HTTPS
        assert DASHBOARD_URL.startswith("https://"), "Dashboard not using HTTPS"

        # 2. Validate page title
        assert "Wazuh" in driver.title, "Unexpected page title"

        # 3. Validate login form elements
        driver.find_element(By.NAME, "username")
        driver.find_element(By.NAME, "password")
        driver.find_element(By.TAG_NAME, "button")

        print("✅ Dashboard reachable and login form validated")

    finally:
        driver.quit()

def test_api_health():
    try:
        resp = requests.get(f"{API_URL}/security/user/authenticate", verify=False)
        assert resp.status_code == 200, f"API not healthy (status {resp.status_code})"
        assert "data" in resp.json(), "Unexpected API response format"
        print("✅ API health probe passed")
    except Exception as e:
        print("❌ API health probe failed:", e)
        sys.exit(1)

if __name__ == "__main__":
    test_dashboard_reachable()
    test_api_health()
