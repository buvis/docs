from adapters import AppItemAdapter, AppListAdapter, ScraperAdapter


class CommandScrape:

    def __init__(self):
        self.applist = AppListAdapter()
        self.app_names = self.applist.list_all_apps()
        self.scraper = ScraperAdapter()

    def execute(self):
        for app_name in self.app_names:
            app = AppItemAdapter(app_name)
            app.scrape(self.scraper)
            app.save()
        self.applist.build_index()
