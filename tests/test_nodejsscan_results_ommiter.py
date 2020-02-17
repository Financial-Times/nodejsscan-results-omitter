from nodejsscan_results_omitter import parse_results
from nodejsscan_results_omitter import remove_issue_if_path_match
from nodejsscan_results_omitter import remove_issue_if_hash_match
from nodejsscan_results_omitter import remove_issue_if_title_match
from nodejsscan_results_omitter import load_json
from nodejsscan_results_omitter import main
import pytest
import json
import os
import sys


@pytest.fixture
def resources():
    with open(os.path.dirname(__file__) + "/fixtures.json", "rb") as f:
        resources = json.load(f)
    return resources


@pytest.fixture
def normal_results():
    with open(os.path.dirname(__file__) + "/results.json", "rb") as f:
        return json.load(f)


@pytest.fixture
def config(resources):
    return resources["config"]


@pytest.fixture
def normal_issue(normal_results):
    return normal_results["sec_issues"]["Application Related"][0]


def test_parse_results(normal_results):
    exit_code = parse_results(normal_results, {})
    assert exit_code == 1


def test_remove_issue_if_path_match(config, normal_issue):
    delete_issue = remove_issue_if_path_match(config["exclude"]["path"], normal_issue)
    assert delete_issue


def test_remove_issue_if_hash_match(config, normal_issue):
    delete_issue = remove_issue_if_hash_match(config["exclude"]["hash"], normal_issue)
    assert delete_issue


def test_remove_issue_if_title_match(config, normal_issue):
    delete_issue = remove_issue_if_title_match(config["exclude"]["title"], normal_issue)
    assert delete_issue


def test_json_file():
    assert load_json(os.path.dirname(__file__) + "/fixtures.json")


def test_unattached_file():
    assert load_json("foo") == {}


def test_invalid_file_type():
    with pytest.raises(json.decoder.JSONDecodeError):
        load_json(os.path.dirname(__file__) + "/../requirements.txt")


def test_main_system_exit():
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
