import json
from pathlib import Path


CURRENT_VERSION = "0.1.24"
NEW_VERSION = "0.1.25"

SCHEMA_DIR = Path("json_schemas")


def update_version_in_json(file_path: Path):
    try:
        with file_path.open("r+", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict) and "version" in data:
                if data["version"] == CURRENT_VERSION:
                    data["version"] = NEW_VERSION
                    f.seek(0)
                    json.dump(data, f, indent=2)
                    f.truncate()
                    print(f"✅ Updated: {file_path}")
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")


def walk_and_update_versions():
    for json_file in SCHEMA_DIR.rglob("*.json"):
        update_version_in_json(json_file)


if __name__ == "__main__":
    walk_and_update_versions()
