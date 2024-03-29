from pathlib import Path

CATALOGUE_DIR = Path("src/catalogue").absolute()
K8SATHOME_SEARCH_URL = "https://nanne.dev/k8s-at-home-search/#/"


class AppItemAdapter:

    def __init__(self, name):
        self.name = name
        self.nice_name = self.name.replace("-", " ").title()
        self.path = Path.joinpath(CATALOGUE_DIR, self.name + ".md")

    def is_catalogued(self):
        return self.path.is_file()

    def scrape(self, scraper):
        self.url_k8sathome_search = K8SATHOME_SEARCH_URL + self.name
        self.helm_charts = scraper.get_helm_charts(self.name)
        self.description = scraper.get_description(self.name)

    def read(self):
        if self.is_catalogued():
            with open(self.path, "r") as app_file:
                lines = app_file.readlines()
            self._parse_markdown(lines)

    def save(self):
        with open(self.path, "w+") as app_file:
            app_file.writelines(self._render_markdown())

    def _parse_markdown(self, lines):
        pass

    def _render_markdown(self):
        charts = ""

        for chart in self.helm_charts:
            charts = charts + f"- [{chart[0]}@{chart[1]}]({chart[2]})\n"
        markdown = f"""# {self.nice_name}

## Description

{self.description}

## k8 at home search

- [{self.name}]({self.url_k8sathome_search})

## Charts

{charts.strip()}
"""

        return markdown
