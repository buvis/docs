import re

from requests import get

URL_README = (
    "https://raw.githubusercontent.com/k8s-at-home/charts/master/charts/README.md"
)


class k8sathomechartsAdapter:

    def __init__(self):
        self.apps = []
        response = get(URL_README)
        res = re.findall(r"\[(.*?)\].*\| (.*?) \|", response.text)
        self.apps = res

    def list_all_apps(self):
        return [name for name, _ in self.apps]

    def get_app_description(self, name):
        for app in self.apps:
            app_name, app_description = app

            if name == name:
                return app_description
