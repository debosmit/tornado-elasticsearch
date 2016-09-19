
from clay import config
from elasticsearch import Elasticsearch
from tornado.testing import gen_test

from tornado_elasticsearch.tests.testlib import load_json_fixture


class ElasticsearchTestCaseMixin:

    es = Elasticsearch([{
        'host': config.get('elasticsearch.host'),
        'port': config.get('elasticsearch.port')}])

    def setup_elasticsearch(self, index_mappings, fixture_name=None, nuke=True, empty=False):
        if nuke:
            self.clear_elasticsearch()

            if not empty:
                self.setup_indices(mappings=index_mappings)

        if fixture_name is not None:
            self.install_json_fixture(fixture_name)

        self.flush_and_refresh()

    def setup_indices(self, mappings):
        for index in mappings:
            if not self.es.indices.exists(index=index):
                self.es.indices.create(index)
            mapping = mappings[index]
            for doc_type in mapping:
                self.es.indices.put_mapping(
                    index=index,
                    doc_type=doc_type,
                    body=mapping[doc_type])

    def install_json_fixture(self, fixture_name):
        items = load_json_fixture(fixture_name)
        for item in items:
            alias = item.get("_alias", None)
            if alias is not None:
                self.es.indices.put_alias(**alias)
                continue
            self.es.index(**item)

        self.flush_and_refresh()

    def clear_elasticsearch(self):
        self.es.indices.delete(index='*')

    def flush_and_refresh(self):
        self.es.indices.flush(wait_if_ongoing=True)
        self.es.indices.refresh(index='*')
