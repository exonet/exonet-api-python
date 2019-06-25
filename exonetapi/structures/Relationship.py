from exonetapi.structures.Relation import Relation


class Relationship(Relation):

    # string Pattern to create the relationship url.
    __urlPattern = '/%s/%s/relationships/%s'
