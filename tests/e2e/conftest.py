import pytest
import threading
import time
import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from werkzeug.serving import make_server
from src.web.app import create_app

class ServerThread(threading.Thread):
    def __init__(self, app, port):
        threading.Thread.__init__(self)
        self.server = make_server('127.0.0.1', port, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()

@pytest.fixture(scope="session")
def server():
    app = create_app({"TESTING": True})
    server = ServerThread(app, 5000)
    server.start()
    time.sleep(1) # wait for server to start
    yield server
    server.shutdown()
    server.join()

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
def base_url(server):
    return "http://127.0.0.1:5000"
