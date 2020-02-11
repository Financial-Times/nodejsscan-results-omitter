from nodejsscan_results_omitter import parse_results
from nodejsscan_results_omitter import remove_paths
import pytest
import json
import os

@pytest.fixture
def resources():
    with open(
            os.path.dirname(__file__) +
            '/fixtures.json', 'rb') as f:
        resources = json.load(f)
    return resources


@pytest.fixture
def normal_results(resources):
    return resources["normal_results"]

@pytest.fixture
def exclude_test_dir_config(resources):
    return resources["exclude_test_dir_config"]

@pytest.fixture
def normal_issue(resources):
    return resources["normal_issue"]

def test_example():
    assert 1==1


def test_parse_results(normal_results):
    exit_code = parse_results(normal_results, {})
    assert exit_code == 1


def test_remove_paths(normal_results, exclude_test_dir_config, normal_issue):
    items_to_delete = remove_paths(normal_results, exclude_test_dir_config["exclude"]["path"], normal_issue)
    assert len(items_to_delete) == 1
    assert items_to_delete[0]["sha2"] == "2809cad0a8c69d250e5c54b056f4a06073bea5eb76000810e661b8316904d87c"
    assert items_to_delete[1]["sha2"] == "da0caf9f5c5eba0384ae977316d05d943e4166cdffdba3b36717d830dd96e407"
