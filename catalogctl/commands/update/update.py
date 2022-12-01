from adapters import (applistAdapter, console, k8sathomechartsAdapter,
                      k8sathomesearchAdapter)


class CommandUpdate:

    def __init__(self):
        self.search = k8sathomesearchAdapter()
        self.k8sathomecharts = k8sathomechartsAdapter()
        self.applist = applistAdapter()

    def execute(self, refresh):
        if refresh:
            app_names_search = self.search.list_all_apps()
            app_names_k8sathomecharts = self.k8sathomecharts.list_all_apps()
            app_names_applist = self.applist.list_all_apps()
            app_names = app_names_search + app_names_k8sathomecharts + app_names_applist
            app_names_unique = list(set(app_names))
            app_names_unique.sort()
            self.applist.save(app_names_unique)
            console.success("List of applications updated")
