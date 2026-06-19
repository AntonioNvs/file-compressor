import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import tempfile

@pytest.fixture
def download_dir():
    with tempfile.TemporaryDirectory() as td:
        yield td

@pytest.fixture
def driver(download_dir):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": False
    }
    options.add_experimental_option("prefs", prefs)
    
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    
    yield driver
    
    driver.quit()

@pytest.fixture
def base_url():
    return "http://localhost:5000"
