import os
import sqlite3
import subprocess
import time
import warnings
from pathlib import Path

import requests
from adapters import console
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from sqlalchemy import MetaData, Table, create_engine
from sqlalchemy.orm import sessionmaker
from webdriver_manager.firefox import GeckoDriverManager

warnings.simplefilter("ignore")

URL_ALL_APPS = "https://nanne.dev/k8s-at-home-search/#/"
URL_REPOS = (
    "https://github.com/Whazor/k8s-at-home-search/releases/latest/download/repos.db.zz"
)
URL_REPOS_EXTENDED = "https://github.com/Whazor/k8s-at-home-search/releases/latest/download/repos-extended.db.zz"


class KaHSearchAdapter:

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(KaHSearchAdapter, cls).__new__(cls)

        return cls.instance

    def __init__(self):

        if not Path("repos.db").is_file():
            self.fetch_database()

        if not Path("repos-extended.db").is_file():
            self.fetch_database()

        self._tables = dict()
        engine_repos = create_engine("sqlite:///repos.db")
        engine_repos_meta = MetaData(engine_repos)
        self._tables["release"] = Table("flux_helm_release",
                                        engine_repos_meta,
                                        autoload=True)
        self._tables["helm"] = Table("flux_helm_repo",
                                     engine_repos_meta,
                                     autoload=True)
        DBSession_repos = sessionmaker(bind=engine_repos)
        self._repos = DBSession_repos()

        engine_extended = create_engine("sqlite:///repos-extended.db")
        engine_extended_meta = MetaData(engine_extended)
        self._tables["release_values"] = Table("flux_helm_release_values",
                                               engine_extended_meta,
                                               autoload=True)
        DBSession_extended = sessionmaker(bind=engine_extended)
        self._extended = DBSession_extended()

    def fetch_database(self):
        try:
            os.remove("repos.db")
        except OSError:
            pass

        try:
            os.remove("repos-extended.db")
        except OSError:
            pass

        repos_db = requests.get(URL_REPOS, allow_redirects=True)
        open("repos.db.zz", "wb").write(repos_db.content)
        cmd = ["pigz", "-d", "-q", "repos.db.zz"]
        subprocess.Popen(cmd)

        repos_extended_db = requests.get(URL_REPOS_EXTENDED,
                                         allow_redirects=True)
        open("repos-extended.db.zz", "wb").write(repos_extended_db.content)
        cmd = ["pigz", "-d", "-q", "repos-extended.db.zz"]
        subprocess.Popen(cmd)

    def list_all_apps(self):
        results = self._repos.query(self._tables["release"])
        app_names = []

        for hr in results.all():
            app_names.append(hr[0])

        return list(set(app_names))

    def get_helm_charts(self, app_name):
        RELEASE = self._tables["release"]
        HELM = self._tables["helm"]
        results = (self._repos.query(RELEASE, HELM).filter(
            RELEASE.c.helm_repo_name == HELM.c.helm_repo_name).filter(
                RELEASE.c.repo_name == HELM.c.repo_name).filter(
                    RELEASE.c.helm_repo_namespace == HELM.c.namespace).filter(
                        RELEASE.c.release_name == app_name).all())

        helm_charts = []

        for hr in results:
            chart_name = hr[1]
            repo_name = hr[9]
            repo_url = hr[13]

            if repo_url not in [h[2] for h in helm_charts]:
                helm_charts.append((chart_name, repo_name, repo_url))

        return helm_charts
