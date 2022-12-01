from pathlib import Path

CATALOGUE_DIR = Path("src/catalogue").absolute()
APP_LIST_PATH = Path.joinpath(CATALOGUE_DIR, "app-list").absolute()
INDEX_PATH = Path.joinpath(CATALOGUE_DIR, "index.md").absolute()


class AppListAdapter:

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

    def build_index(self):
        markdown = """# Catalogue

Here I maintain the information about applications I run or could run in my clusters.

## Sorted by name

"""

        for app in self.apps:
            markdown = markdown + f"- [{app}]({app})\n"

        with open(INDEX_PATH, "w+") as app_index:
            app_index.writelines(markdown)
