
import json
import re
from os import environ, path


def load_json_fixture(name):
    json_comment_expr = re.compile('^\s+\/\/')
    lines = _load_fixture(name).split("\n")
    data = '\n'.join(
        [line for line in lines if not json_comment_expr.match(line)]
    )
    return json.loads(data)


def _load_fixture(name):
    fixture_path = environ.get('TEST_FIXTURES_PATH')
    if not fixture_path:
        raise KeyError(
            'Environment variable `TEST_FIXTURES_PATH` is not specified; '
            'TEST_FIXTURES_PATH is the path to directories that hold fixture files.')
    filepath = path.join(fixture_path, name)
    if path.isfile(filepath):
        with open(filepath, "rb") as f:
            return f.read()
