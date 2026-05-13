import json
import os
import shutil

PROJECT_DIR = "/home/user/inconvo-app"
USERS_JSON = os.path.join(PROJECT_DIR, "users.json")
NODE_MODULES_SDK = os.path.join(PROJECT_DIR, "node_modules", "@inconvoai", "node")


def test_node_available():
    assert shutil.which("node") is not None, "node binary not found in PATH."
    assert shutil.which("npm") is not None, "npm binary not found in PATH."


def test_project_directory_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."


def test_users_json_present_with_two_ids():
    assert os.path.isfile(USERS_JSON), f"Expected users.json at {USERS_JSON}."
    with open(USERS_JSON, "r") as f:
        data = json.load(f)
    assert isinstance(data, list), f"users.json must contain a JSON array, got: {type(data).__name__}."
    assert data == ["alice-001", "bob-002"], (
        f"users.json must equal [\"alice-001\", \"bob-002\"], got: {data}."
    )


def test_inconvo_sdk_installed():
    package_json = os.path.join(PROJECT_DIR, "package.json")
    assert os.path.isfile(package_json), f"package.json not found at {package_json}."
    with open(package_json, "r") as f:
        content = f.read()
    assert "@inconvoai/node" in content, "Expected @inconvoai/node listed in package.json."
    assert os.path.isdir(NODE_MODULES_SDK), (
        f"@inconvoai/node not installed under {NODE_MODULES_SDK}."
    )
