import unittest
from unittest import mock
from unittest.mock import call

from exonetapi.result.Parser import Parser


class testParser(unittest.TestCase):
    @mock.patch('exonetapi.create_resource.create_resource', create=True)
    def test_parse_list(self, mock_create_resource):
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

        Parser(json_data_list).parse()

        mock_create_resource.assert_has_calls([
            call('comments', {'subject': 'Can you help me?'}, 'DV6axK4GwNEb', {'author': {
                'links': {'self': 'https://api.exonet.nl/comments/DV6axK4GwNEb/relationships/author',
                          'related': 'https://api.exonet.nl/comments/DV6axK4GwNEb/author'},
                'data': {'type': 'employees', 'id': 'ypPe9wqp7gxb'}}}),
            call('comments', {'subject': 'Yes I can!'}, 'zWX9r7exA28G', {'author': {
                'links': {'self': 'https://api.exonet.nl/comments/zWX9r7exA28G/relationships/author',
                          'related': 'https://api.exonet.nl/comments/zWX9r7exA28G/author'},
                'data': {'type': 'employees', 'id': 'dbJEx7go7WN0'}}})
        ])

    @mock.patch('exonetapi.create_resource.create_resource', create=True)
    def test_parse_single(self, mock_create_resource):
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

        Parser(json_data_list).parse()

        mock_create_resource.assert_has_calls([
            call('comments', {'subject': 'Can you help me?'}, 'DV6axK4GwNEb', {'author': {
                'links': {'self': 'https://api.exonet.nl/comments/DV6axK4GwNEb/relationships/author',
                          'related': 'https://api.exonet.nl/comments/DV6axK4GwNEb/author'},
                'data': {'type': 'employees', 'id': 'ypPe9wqp7gxb'}}}),
        ])


if __name__ == '__main__':
    unittest.main()
