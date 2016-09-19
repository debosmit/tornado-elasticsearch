import os
import re
import webbrowser

try:
    from fabric.api import env, local, task, shell_env
    from fabric.colors import green
except ImportError as e:
    print("Install fabric using `pip install fabric`")
    raise
from pathlib import Path

# paths for virtualenv
env.directory = re.sub(r'(tornado-elasticsearch).*$', r'\1', os.getcwd())
env.activate = '. %s/env/bin/activate' % env.directory

DEFAULT_ENVIRONMENT = 'local'
TEST_FIXTURES_PATH = Path(__file__).resolve().parent / 'tornado_elasticsearch' / 'tests' / 'fixtures'


@task
def clean():
    """Remove logfiles, test files and .pyc files."""
    # Ignore hidden files and folder
    local("find . \( ! -regex '.*/\..*/..*' \) -type f -name '*.pyc' -exec rm '{}' +")
    local("rm -rf cover .coverage* htmlcov *.log")


@task
def setup():
    """Bootstrap the environment."""
    print(green('\nInstalling requirements'))
    cmd = "pip install -r requirements.txt"
    local(cmd)


@task
def test(environment=DEFAULT_ENVIRONMENT):
    """Execute unit tests"""
    env = {
        'CLAY_CONFIG': "%s/config/%s.yaml" % (os.getcwd(), environment),
        'TEST_FIXTURES_PATH': str(TEST_FIXTURES_PATH)
    }
    with shell_env(**env):
        cmd = "nosetests -v"
        local(cmd)


@task
def coverage(environment=DEFAULT_ENVIRONMENT):
    """Execute unit tests with coverage report"""
    print(green("Executing unit tests"))
    env = {
        'CLAY_CONFIG': "%s/config/%s.yaml" % (os.getcwd(), environment),
        'TEST_FIXTURES_PATH': str(TEST_FIXTURES_PATH)
    }
    with shell_env(**env):
        local("nosetests --with-coverage "
              "--cover-package=tornado-elasticsearch "
              "--cover-html "
              "--cover-inclusive ")
        coverdir = Path(__file__).parent.resolve() / "cover/index.html"
        webbrowser.open_new("file://" + str(coverdir))
