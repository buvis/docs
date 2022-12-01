from adapters import (AppListAdapter, KaHChartsAdapter, KaHSearchAdapter,
                      console)


class CommandDiscover:

    def __init__(self):
        self.kah_search = KaHSearchAdapter()
        self.kah_charts = KaHChartsAdapter()
        self.applist = AppListAdapter()

    def execute(self):
        app_names_search = self.kah_search.list_all_apps()
        app_names_kah_charts = self.kah_charts.list_all_apps()
        app_names_applist = self.applist.list_all_apps()
        app_names = app_names_search + app_names_kah_charts + app_names_applist
        app_names_unique = list(set(app_names))
        app_names_unique.sort()
        self.applist.save(app_names_unique)
        additions = set(app_names_unique) - set(app_names_applist)

        if len(additions) > 0:
            console.success(f"Additions to catalogue: {', '.join(additions)}")
        else:
            console.success("Applications list is up to date")
