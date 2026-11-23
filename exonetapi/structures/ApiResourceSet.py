from __future__ import annotations

from typing import TYPE_CHECKING, Any, Self

import exonetapi

if TYPE_CHECKING:
    from exonetapi.structures.ApiResource import ApiResource


class ApiResourceSet:
    """A page of resources from the API, with its meta data and links."""

    def __init__(self) -> None:
        self.__resources: list[ApiResource] = []
        self.__meta: dict[str, Any] | None = {}
        self.__links: dict[str, Any] | None = {}
        self.__iter_current = 0

    def total(self) -> int | None:
        return self.__meta.get("resources", {"total": None}).get("total")

    def links(self) -> dict[str, Any] | None:
        return self.__links

    def meta(self) -> dict[str, Any] | None:
        return self.__meta

    def next_page(self) -> ApiResource | ApiResourceSet | None:
        return self.__get_link("next")

    def previous_page(self) -> ApiResource | ApiResourceSet | None:
        return self.__get_link("prev")

    def first_page(self) -> ApiResource | ApiResourceSet | None:
        return self.__get_link("first")

    def last_page(self) -> ApiResource | ApiResourceSet | None:
        return self.__get_link("last")

    def add_resource(self, resource: ApiResource | list[ApiResource]) -> None:
        if isinstance(resource, list):
            self.__resources.extend(resource)
        else:
            self.__resources.append(resource)

    def set_meta(self, meta: dict[str, Any] | None) -> Self:
        self.__meta = meta

        return self

    def set_links(self, links: dict[str, Any] | None) -> Self:
        self.__links = links

        return self

    def resources(self) -> list[ApiResource]:
        return self.__resources

    def __get_link(self, link_name: str) -> ApiResource | ApiResourceSet | None:
        request = exonetapi.RequestBuilder()
        host = exonetapi.Client().get_host()
        link_value = self.__links.get(link_name)

        if link_value is not None:
            return request.get(link_value.replace(f"{host}/", ""))
        return None

    def __len__(self) -> int:
        """Count the resources in this set."""
        return len(self.__resources)

    def __getitem__(self, index: int) -> ApiResource:
        """Return the resource at this position in the set."""
        return self.__resources[index]

    def __iter__(self) -> Self:
        """Iterate over the resources in this set."""
        return self

    def __next__(self) -> ApiResource:
        """Return the next resource, and start over once the set is exhausted."""
        current = self.__iter_current
        self.__iter_current += 1

        if len(self.__resources) > current:
            return self.__resources[current]

        self.__iter_current = 0

        raise StopIteration
