import time

from adapters import console, k8sathomesearchAdapter


class CommandUpdate:

    def __init__(self):
        self.search = k8sathomesearchAdapter()

    def execute(self):
        apps = self.search.get_apps()
        print(apps)
