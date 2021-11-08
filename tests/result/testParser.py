import unittest

from tests.testCase import testCase
from exonetapi.result import Parser


class testParser(testCase):
    def test_parse_list(self):
        json_data_list = """
        {
          "data": [
            {
              "type": "comments",
              "id": "DV6axK4GwNEb",
              "attributes": {
                "subject": "Can you help me?"
              },
              "relationships": {
                "author": {
                  "links": {
                    "self": "https://api.exonet.nl/comments/DV6axK4GwNEb/relationships/author",
                    "related": "https://api.exonet.nl/comments/DV6axK4GwNEb/author"
                  },
                  "data": {
                    "type": "employees",
                    "id": "ypPe9wqp7gxb"
                  }
                }
              }
            },
            {
              "type": "comments",
              "id": "zWX9r7exA28G",
              "attributes": {
                "subject": "Yes I can!"
              },
              "relationships": {
                "author": {
                  "links": {
                    "self": "https://api.exonet.nl/comments/zWX9r7exA28G/relationships/author",
                    "related": "https://api.exonet.nl/comments/zWX9r7exA28G/author"
                  },
                  "data": {
                    "type": "employees",
                    "id": "dbJEx7go7WN0"
                  }
                }
              }
            }
          ]
        }
        """

        result = Parser(str.encode(json_data_list)).parse().resources()

        self.assertEqual(result[0].id(), 'DV6axK4GwNEb')
        self.assertEqual(result[0].type(), 'comments')

        self.assertEqual(result[1].id(), 'zWX9r7exA28G')
        self.assertEqual(result[1].type(), 'comments')

    def test_parse_single(self):
        json_data_list = """
        {
          "data":
            {
              "type": "comments",
              "id": "DV6axK4GwNEb",
              "attributes": {
                "subject": "Can you help me?"
              },
              "relationships": {
                "author": {
                  "links": {
                    "self": "https://api.exonet.nl/comments/DV6axK4GwNEb/relationships/author",
                    "related": "https://api.exonet.nl/comments/DV6axK4GwNEb/author"
                  },
                  "data": {
                    "type": "employees",
                    "id": "ypPe9wqp7gxb"
                  }
                }
              }
            }
        }
        """

        result = Parser(str.encode(json_data_list)).parse()

        self.assertEqual(result.id(), 'DV6axK4GwNEb')
        self.assertEqual(result.type(), 'comments')

    def test_parse_single_with_multi_relation(self):
        json_data_list = """
        {
          "data": {
            "type": "comments",
            "id": "DV6axK4GwNEb",
            "attributes": {
              "subject": "Can you help me?"
            },
            "relationships": {
              "tags": {
                "links": {
                  "self": "https://api.exonet.nl/comments/DV6axK4GwNEb/relationships/tags",
                  "related": "https://api.exonet.nl/comments/DV6axK4GwNEb/tags"
                },
                "data": [
                  {
                    "type": "tags",
                    "id": "ABC"
                  },
                  {
                    "type": "tags",
                    "id": "XYZ"
                  }
                ]
              }
            }
          }
        }
        """

        result = Parser(str.encode(json_data_list)).parse().relationship('tags').get_resource_identifiers()

        self.assertEqual(len(result), 2)

        def test_parse_single_with_multi_relation(self):
            json_data_list = """
            {
              "data":
                {
                  "type": "comments",
                  "id": "DV6axK4GwNEb",
                  "attributes": {
                    "subject": "Can you help me?"
                  },
                  "relationships": {
                    "tags": {
                      "links": {
                        "self": "https://api.exonet.nl/comments/DV6axK4GwNEb/relationships/tags",
                        "related": "https://api.exonet.nl/comments/DV6axK4GwNEb/tags"
                      },
                      "data": [
                          {
                            "type": "tags",
                            "id": "ABC"
                          },
                          {
                            "type": "tags",
                            "id": "XYZ"
                          }

                      ]
                    }
                  }
                }
            }
            """

            result = Parser(json_data_list).parse().relationship('tags').get_resource_identifiers()

            self.assertEqual(len(result), 2)


if __name__ == '__main__':
    unittest.main()
