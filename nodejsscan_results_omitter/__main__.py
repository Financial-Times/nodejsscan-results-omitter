import json
import os
import sys
from fnmatch import fnmatch
from pprint import pprint

CONFIG_FILE = ".nodejsscan.json"
RESULTS_FILE = "results.json"

cwd = os.getcwd()


def load_json(file_name):
    try:
        with open(file_name, "r") as f:
            content = json.load(f)
        return content
    except FileNotFoundError:
        return {}


def remove_issue_if_path_match(paths, issue):
    for path in paths:
        if fnmatch(name=issue["path"], pat=f"{path}"):
            return True
    return False


def remove_issue_if_hash_match(hashes, issue):
    for issue_hash in hashes:
        if issue["sha2"] == issue_hash:
            return True
    return False


def remove_issue_if_title_match(titles, issue):
    for title in titles:
        if issue["title"] == title:
            return True
    return False


def parse_results(results, config):
    exit_code = 0
    items_to_delete = []

    excluded_paths = config.get("exclude", {}).get("path", [])
    excluded_hashes = config.get("exclude", {}).get("hash", [])
    excluded_titles = config.get("exclude", {}).get("title", [])

    cwd = os.getcwd()
    for category in results["sec_issues"].keys():
        for issue in results["sec_issues"][category]:
            if (
                remove_issue_if_path_match(excluded_paths, issue)
                or remove_issue_if_hash_match(excluded_hashes, issue)
                or remove_issue_if_title_match(excluded_titles, issue)
            ):
                items_to_delete.append(issue)

        results["total_count"]["sec"] -= len(items_to_delete)
        results["sec_issues"][category] = [
            issue
            for issue in results["sec_issues"][category]
            if issue not in items_to_delete
        ]
        items_to_delete = []
    if results["total_count"]["sec"] > 0:
        exit_code = 1

    pprint(results)
    return exit_code


def main():
    config = load_json(CONFIG_FILE)
    results = load_json(RESULTS_FILE)
    if not results:
        print(f"Missing {RESULTS_FILE} file")
        sys.exit(1)

    sys.exit(parse_results(results, config))


if __name__ == "__main__":
    main()
