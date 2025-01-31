import os
import pathlib
from typing import Any
import json
import shutil

GH_PAGE_PATH = os.getenv("GH_PAGE_PATH") or exit ("GitHub page directory is required")
MAIN_INDEX_PATH = "./resources/index.html"
ACTION_PATH = os.getenv("ACTION_PATH") or exit ("Action path is required")

gh_page_path = pathlib.Path(GH_PAGE_PATH)
action_path = pathlib.Path(ACTION_PATH)
main_index_path = action_path / pathlib.Path(MAIN_INDEX_PATH)

def get_all_metadata() -> list[dict[str,Any]]:
    result: list[dict[str,Any]] = []
    for dir in os.listdir(gh_page_path):
        dir_path = gh_page_path / dir
        if os.path.isdir(dir_path):
            metadata_path = dir_path / "metadata.json"
            if metadata_path.exists():
                with open(metadata_path, "r") as f:
                    result.append(json.load(f))
    return result

def generate_minifest():
    # Validate github page path directory
    if not gh_page_path.exists():
        gh_page_path.mkdir(parents=True)
    if not gh_page_path.is_dir():
        exit(f"{gh_page_path} is not a directory")
    
    if not main_index_path.is_file():
        exit(f"{main_index_path} does not exist")

    manifest = get_all_metadata()
    manifest.sort(key=lambda x: x.get("Timestamp",""), reverse=True)

    shutil.copy(main_index_path, gh_page_path / "index.html")
    with open(gh_page_path / "manifest.json", "w") as f:
        json.dump(manifest, f, indent=4)

    print(f"Manifest generated at {gh_page_path}")

if __name__ == "__main__":
    generate_minifest()