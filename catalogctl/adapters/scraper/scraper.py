from adapters import KaHChartsAdapter, KaHSearchAdapter


class ScraperAdapter:

    def __init__(self):
        self.kah_charts = KaHChartsAdapter()
        self.kah_search = KaHSearchAdapter()

    def get_helm_charts(self, app_name):
        return self.kah_search.get_helm_charts(app_name)

    def get_description(self, app_name):
        kah_charts_description = self.kah_charts.get_app_description(app_name)

        if kah_charts_description:
            if not kah_charts_description.endswith("."):
                kah_charts_description = kah_charts_description + "."

            return kah_charts_description
        else:
            return "No description provided."
