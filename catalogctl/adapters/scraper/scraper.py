from adapters import k8sathomechartsAdapter


class ScraperAdapter:

    def __init__(self):
        self.kah_charts = k8sathomechartsAdapter()

    def get_helm_releases(self):
        pass

    def get_description(self, app_name):
        kah_charts_description = self.kah_charts.get_app_description(app_name)

        if kah_charts_description:
            return kah_charts_description
        else:
            return "No description provided."
