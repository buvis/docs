import time

from adapters import console
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager

URL_ALL_APPS = "https://nanne.dev/k8s-at-home-search/#/"


class KaHSearchAdapter:

    def __init__(self):
        options = Options()
        options.headless = True
        self.browser = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=options,
        )

    def list_all_apps(self):
        self.browser.get(URL_ALL_APPS)
        WebDriverWait(self.browser, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//*[text()='...']")))
        soup = BeautifulSoup(self.browser.page_source, "html.parser")
        app_links = soup.find_all("a", class_="word-cloud-word")
        collapsed_count = len(app_links)
        expanded_count = len(app_links)
        WebDriverWait(self.browser, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[text()='...']"))).click()

        while collapsed_count == expanded_count:
            time.sleep(1)
            soup = BeautifulSoup(self.browser.page_source, "html.parser")
            [s.extract() for s in soup("svg")]
            [s.extract() for s in soup("span")]
            app_links = soup.find_all("a", class_="word-cloud-word")
            expanded_count = len(app_links)

        self.browser.quit()

        for link in app_links:
            if not link.string:
                console.failure(f"Couldn't get the app name from {link}")

        return [link.string.strip() for link in app_links]
