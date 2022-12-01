from adapters import (AppListAdapter, console, k8sathomechartsAdapter,
                      k8sathomesearchAdapter)


class CommandDiscover:

    def __init__(self):
        self.search = k8sathomesearchAdapter()
        self.k8sathomecharts = k8sathomechartsAdapter()
        self.applist = AppListAdapter()

    def execute(self):
        app_names_search = self.search.list_all_apps()
        app_names_k8sathomecharts = self.k8sathomecharts.list_all_apps()
        app_names_applist = self.applist.list_all_apps()
        app_names = app_names_search + app_names_k8sathomecharts + app_names_applist
        app_names_unique = list(set(app_names))
        app_names_unique.sort()
        self.applist.save(app_names_unique)
        additions = set(app_names_unique) - set(app_names_applist)

        if len(additions) > 0:
            console.success(f"Additions to catalogue: {', '.join(additions)}")
        else:
            console.success("Applications list is up to date")
