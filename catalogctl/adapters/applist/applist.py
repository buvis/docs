from pathlib import Path

APP_LIST_PATH = Path("src/catalogue/app-list").absolute()


class applistAdapter:

    def __init__(self):
        self.apps = []
        with open(APP_LIST_PATH, "r") as app_list:
            for line in app_list:
                self.apps.append(line.strip())

    def list_all_apps(self):
        return self.apps

    def save(self, app_names):
        with open(APP_LIST_PATH, "w+") as app_list:
            for app in app_names:
                app_list.write(app + "\n")
