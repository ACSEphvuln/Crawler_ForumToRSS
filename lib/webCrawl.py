import time
from selenium import webdriver
import urllib.request

class StaticPageGetter:
    def __init__(self, url) -> None:
        self.url = url

    def getPage(self, waitTime=5):
        req = urllib.request.Request(self.url)
        req.add_header('User-agent', 'Chrome 111.0.0, Windows 10/11')
        page = urllib.request.urlopen(req,timeout=waitTime)
        return page.read()

class DynamicPageGetter:
    def __init__(self, url) -> None:
        self.url = url
        self.driver = None
    
    def initDriver(self):
        self.driver = webdriver.Firefox()

    def stopDriver(self):
        self.driver.quit()
        self.driver = None

    def getPage(self, waitTime=20):
        self.initDriver()

        # Bypass dos-protection
        self.driver.get(self.url)
        time.sleep(waitTime)

        # Get the HTML content of the page
        html_content = self.driver.page_source

        self.stopDriver()

        return html_content