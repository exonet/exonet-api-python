import exonetapi


class ApiResourceSet:
    def __init__(self):
        self.__resources = []
        self.__meta = {}
        self.__links = {}
        self.__iter_current = 0

    def total(self):
        return self.__meta.get('resources', {"total": None}).get('total')

    def links(self):
        return self.__links

    def meta(self):
        return self.__meta

    def next_page(self):
        return self.__get_link('next')

    def previous_page(self):
        return self.__get_link('prev')

    def first_page(self):
        return self.__get_link('first')

    def last_page(self):
        return self.__get_link('last')

    def add_resource(self, resource):
        if isinstance(resource, list):
            self.__resources.extend(resource)
        else:
            self.__resources.append(resource)

    def set_meta(self, meta):
        self.__meta = meta

        return self

    def set_links(self, links):
        self.__links = links

        return self

    def resources(self):
        return self.__resources

    def __get_link(self, link_name):
        request = exonetapi.RequestBuilder()
        host = exonetapi.Client().get_host()
        link_value = self.__links.get(link_name)

        if link_value is not None:
            return request.get(link_value.replace('{}/'.format(host), ''))
        else:
            return None

    def __len__(self):
        return len(self.__resources)

    def __iter__(self):
        return self

    def __next__(self):
        current = self.__iter_current
        self.__iter_current += 1

        if len(self.__resources) > current:
            return self.__resources[current]

        self.__iter_current = 0

        raise StopIteration
