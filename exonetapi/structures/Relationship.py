from exonetapi.structures.Relation import Relation


class Relationship(Relation):
    """The relationship of a resource, as opposed to the related resources."""

    # string Pattern to create the relationship url.
    __urlPattern = "/%s/%s/relationships/%s"
