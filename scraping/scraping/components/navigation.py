from typing import List

import urllib.parse


def get_navigation(base):

    class Navigation(base):

        def __init__(self, path, route= None, max_pages = None) -> None:
            super().__init__(path)
            self.route = route
            self.page = 1
            self.max_pages = max_pages

        def get(self,response):
            data = super().get(response)
            if self.route is not None and data is not None:
                parsed = urllib.parse.urlparse(response.url)
                params = urllib.parse.parse_qsl(parsed.query)

                if len(params) == 0:
                    data = f'{response.url}?{self.route}={2}'
                else:
                    url_dict = {}
                    param_found = False
                    for key,value in params:
                        if key == self.route:
                            param_found = True
                            value = int(value) + 1
                        url_dict[key] = value
                    base_url = response.url.split("?")[0]
                    data =  f'{base_url}?' + urllib.parse.urlencode(url_dict)

                    if param_found is False:
                        data = f'{data}&{self.route}={2}'

            return data     

    return Navigation