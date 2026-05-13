import os
import json
import shutil
import pytest

PROJECT_DIR = "/home/user/inconvo-app"


def test_node_installed():
    assert shutil.which("node") is not None, "node binary not found in PATH."
    assert shutil.which("npm") is not None, "npm binary not found in PATH."


def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."


def test_package_json_exists_with_required_dependencies():
    package_json_path = os.path.join(PROJECT_DIR, "package.json")
    assert os.path.isfile(package_json_path), f"package.json not found at {package_json_path}"

    with open(package_json_path, "r") as f:
        try:
            pkg = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("package.json is not valid JSON")

    deps = {}
    deps.update(pkg.get("dependencies") or {})
    deps.update(pkg.get("devDependencies") or {})
    assert "@inconvoai/node" in deps, "Expected '@inconvoai/node' dependency in package.json"
    assert "dotenv" in deps, "Expected 'dotenv' dependency in package.json"


def test_node_modules_inconvo_installed():
    inconvo_pkg = os.path.join(PROJECT_DIR, "node_modules", "@inconvoai", "node")
    assert os.path.isdir(inconvo_pkg), \
        f"@inconvoai/node module not installed at {inconvo_pkg}"


def test_env_file_present_with_required_vars():
    env_path = os.path.join(PROJECT_DIR, ".env")
    assert os.path.isfile(env_path), f".env file not found at {env_path}"

    with open(env_path, "r") as f:
        content = f.read()
    assert "INCONVO_API_KEY" in content, "Expected INCONVO_API_KEY referenced in .env"
    assert "INCONVO_AGENT_ID" in content, "Expected INCONVO_AGENT_ID referenced in .env"
    assert "INCONVO_DB_URL" in content, "Expected INCONVO_DB_URL referenced in .env"
