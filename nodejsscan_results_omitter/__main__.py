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


def remove_paths(results, paths, issue):
    items_to_delete = []
    for path in paths:
        if fnmatch(name=issue["path"], pat=f"{cwd}/{path}"):
            items_to_delete.append(issue)
            results["total_count"]["sec"] -= 1
    return items_to_delete

def parse_results(results, config):
    exit_code = 0
    items_to_delete = []

    excluded_paths = config.get("exclude", {}).get("path", [])
    excluded_hashes = config.get("exclude", {}).get("hash", [])
    excluded_titles = config.get("exclude", {}).get("title", [])

    cwd = os.getcwd()
    for category in results['sec_issues'].keys():
        for issue in results['sec_issues'][category]:
            for path in excluded_paths:
                if fnmatch(issue["path"], f"{cwd}/{path}"):
                    items_to_delete.append(issue)
                    results["total_count"]["sec"] -= 1
            for issue_hash in excluded_hashes:
                if issue["sha2"] == issue_hash:
                    items_to_delete.append(issue)
                    results["total_count"]["sec"] -= 1
            for title in excluded_titles:
                if issue["title"] == title:
                    items_to_delete.append(issue)
                    results["total_count"]["sec"] -= 1
        results['sec_issues'][category] = [
            issue
            for issue in results['sec_issues'][category]
            if issue not in items_to_delete
        ]
        items_to_delete = []              
    if results['total_count']['sec'] > 0:
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

