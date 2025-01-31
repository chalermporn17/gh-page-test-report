import json
import os
import pathlib
from datetime import datetime, timezone
import re
import shutil
from typing import Any

REPORT_NAME = os.getenv("REPORT_NAME") or exit ("Report name is required")
REPORT_DIRECTORY_NAME = os.getenv("REPORT_DIRECTORY_NAME") or exit ("Report directory name is required")
COMMIT_SHA = os.getenv("COMMIT_SHA") or exit ("Commit SHA is required")
RUN_NUMBER = os.getenv("RUN_NUMBER") or exit ("Run number is required")
GH_PAGE_PATH = os.getenv("GH_PAGE_PATH") or exit ("GitHub page directory is required")
ACTION_PATH = os.getenv("ACTION_PATH") or exit ("Action path is required")

gh_page_path = pathlib.Path(GH_PAGE_PATH)
action_path = pathlib.Path(ACTION_PATH)

def get_report_path() -> dict[str,str]:
    result: dict[str,str] = {}
    for env in os.environ:
        matched = re.findall(r"^TEST_REPORT_([a-zA-Z0-9_\-]+)_PATH$", env)
        if matched:
            result[matched[0].lower()] = os.getenv(env) or exit(f"Environment variable {env} is passed but empty")
    return result

def generate_report():
    # Validate github page path directory
    if not gh_page_path.exists():
        gh_page_path.mkdir(parents=True)
    if not gh_page_path.is_dir():
        print(f"{gh_page_path} is not a directory")
        return
    
    # Create report directory
    report_path = gh_page_path / REPORT_DIRECTORY_NAME
    if report_path.exists():
        exit(f"Report directory {report_path} already exists") 
    report_path.mkdir(parents=True)

    # Get individual test report paths from input
    test_report_paths = get_report_path()

    # Copy individual test reports to report directory
    for test_report_type, test_report_path in test_report_paths.items():
        shutil.copytree(test_report_path, report_path / test_report_type)

    # Create report metadata
    metadata: dict[str, Any] = {
        "name": REPORT_NAME,
        "commit_sha": COMMIT_SHA,
        "run_number": RUN_NUMBER,
        "timestamp": datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S'),
        "dirName": REPORT_DIRECTORY_NAME,
        "reports": list(test_report_paths.keys())
    }

    # Write metadata to report directory
    with open(report_path / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=4)

    print(f"Report generated at {report_path}")

if __name__ == "__main__":
    generate_report()