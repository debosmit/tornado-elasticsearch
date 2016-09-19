
import unittest

from tornado_elasticsearch.tests.testlib.es_mixin import ElasticsearchTestCaseMixin


class TestMixin(unittest.TestCase, ElasticsearchTestCaseMixin):

    def setUp(self):
        self.maxDiff = None

    def test_setup_elasticsearch(self):
        mapping = {
            "uid": {
                "_all": {
                    "enabled": False
                },
                "properties": {
                    "uid": {
                        "type": "string",
                        "index": "not_analyzed"
                    }
                }
            }
        }

        index_mappings = {'index_name': mapping}
        self.setup_elasticsearch(index_mappings=index_mappings)

        index_exists = self.es.indices.exists(index='index_name')
        self.assertTrue(index_exists)

        index_mapping = self.es.indices.get_mapping(index='index_name')
        expected_mapping = {
            'index_name': {
                'mappings': mapping
            }
        }
        self.assertDictEqual(index_mapping, expected_mapping)
