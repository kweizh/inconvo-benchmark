import os
import shutil
import json
import pytest

PROJECT_DIR = "/home/user/inconvo-app"
PACKAGE_JSON = os.path.join(PROJECT_DIR, "package.json")
NODE_MODULES = os.path.join(PROJECT_DIR, "node_modules")
INCONVO_PKG = os.path.join(NODE_MODULES, "@inconvoai", "node")


def test_node_available():
    assert shutil.which("node") is not None, "node binary not found in PATH."
    assert shutil.which("npm") is not None, "npm binary not found in PATH."


def test_project_directory_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."


def test_package_json_exists():
    assert os.path.isfile(PACKAGE_JSON), f"package.json not found at {PACKAGE_JSON}"


def test_package_json_lists_required_dependencies():
    with open(PACKAGE_JSON, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"package.json at {PACKAGE_JSON} is not valid JSON")

    deps = {}
    deps.update(data.get("dependencies", {}) or {})
    deps.update(data.get("devDependencies", {}) or {})

    assert "@inconvoai/node" in deps, \
        f"Expected '@inconvoai/node' in package.json dependencies, got: {deps}"
    assert "dotenv" in deps, \
        f"Expected 'dotenv' in package.json dependencies, got: {deps}"


def test_node_modules_installed():
    assert os.path.isdir(NODE_MODULES), \
        f"node_modules directory not found at {NODE_MODULES}"
    assert os.path.isdir(INCONVO_PKG), \
        f"@inconvoai/node package not installed at {INCONVO_PKG}"
