from __future__ import annotations

from typing import TYPE_CHECKING, Any, Self, TypeAlias

if TYPE_CHECKING:
    from collections.abc import Callable

    from exonetapi.structures.ApiResourceIdentifier import ApiResourceIdentifier
    from exonetapi.structures.ApiResourceSet import ApiResourceSet

    ResourceIdentifiers: TypeAlias = (
        ApiResourceIdentifier | ApiResourceSet | list[ApiResourceIdentifier] | None
    )


class Relation:
    """A relation of a resource, which requests on it are made through."""

    # string Pattern to create the relation url.
    __urlPattern = "/%s/%s/%s"

    def __init__(
        self, relation_name: str, origin_type: str, origin_id: str | None
    ) -> None:
        """Relation constructor.

        :param str relation_name: The name of the relation.
        :param str origin_type: The resource type of the origin resource.
        :param str origin_id: The resource ID of the origin resource.
        """
        self.__name = relation_name
        self.__url = self.__urlPattern % (origin_type, origin_id, relation_name)

        # ApiResourceSet|ApiResourceIdentifier The related resource identifier or a
        # ApiResourceSet.
        self.__resourceIdentifiers: ResourceIdentifiers = None

        # RequestBuilder imports the structures, so it can only be imported here.
        from exonetapi import RequestBuilder  # noqa: PLC0415

        self.__request = RequestBuilder(self.__url)

    def __len__(self) -> int:
        """Count the related resource identifiers."""
        if self.__resourceIdentifiers:
            return len(self.__resourceIdentifiers)

        return 0

    def __getattr__(self, name: str) -> Callable[[], Any]:
        """Pass a call to an unknown method on to the request for this relation."""

        def method() -> Any:
            return getattr(self.__request, name)()

        return method

    def get_resource_identifiers(self) -> ResourceIdentifiers:
        """Get the resource identifiers for this relation.

        :return ApiResourceSet|ApiResourceIdentifier: The resource identifier or a
                                                      resource set.
        """
        return self.__resourceIdentifiers

    def set_resource_identifiers(self, new_relationship: ResourceIdentifiers) -> Self:
        """Replace the related resource identifiers with new data.

        :param ApiResourceSet|ApiResourceIdentifier new_relationship: A new resource
                                                                      identifier or a
        new resource set.
        :return self:
        """
        self.__resourceIdentifiers = new_relationship

        return self
