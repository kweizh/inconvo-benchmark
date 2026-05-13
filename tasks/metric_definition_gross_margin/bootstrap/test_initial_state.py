import os
import shutil
import pytest

PROJECT_DIR = "/home/user/inconvo-app"


def test_node_available():
    assert shutil.which("node") is not None, "node binary not found in PATH."
    assert shutil.which("npm") is not None, "npm binary not found in PATH."


def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), \
        f"Project directory {PROJECT_DIR} does not exist."


def test_package_json_has_inconvo_sdk():
    package_json_path = os.path.join(PROJECT_DIR, "package.json")
    assert os.path.isfile(package_json_path), \
        f"package.json not found at {package_json_path}"

    with open(package_json_path, "r") as f:
        content = f.read()

    assert "@inconvoai/node" in content, \
        "Expected '@inconvoai/node' to be declared as a dependency in package.json."
    assert "dotenv" in content, \
        "Expected 'dotenv' to be declared as a dependency in package.json."


def test_inconvo_sdk_installed_in_node_modules():
    sdk_path = os.path.join(PROJECT_DIR, "node_modules", "@inconvoai", "node")
    assert os.path.isdir(sdk_path), \
        f"Expected @inconvoai/node SDK installed at {sdk_path}"


def test_env_file_exists_with_required_vars():
    env_path = os.path.join(PROJECT_DIR, ".env")
    assert os.path.isfile(env_path), f".env file not found at {env_path}"

    with open(env_path, "r") as f:
        content = f.read()

    assert "INCONVO_API_KEY" in content, \
        "Expected INCONVO_API_KEY in .env file."
    assert "INCONVO_AGENT_ID" in content, \
        "Expected INCONVO_AGENT_ID in .env file."
    assert "INCONVO_DB_URL" in content, \
        "Expected INCONVO_DB_URL in .env file."


def test_inconvo_yaml_exists():
    yaml_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    assert os.path.isfile(yaml_path), \
        f"inconvo.yaml not found at {yaml_path}"


def test_inconvo_yaml_contains_orders_and_customers_tables():
    yaml_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    with open(yaml_path, "r") as f:
        content = f.read()

    assert "orders" in content, \
        "Expected 'orders' table definition in inconvo.yaml."
    assert "customers" in content, \
        "Expected 'customers' table definition in inconvo.yaml."
    assert "total_amount" in content, \
        "Expected 'total_amount' field in initial inconvo.yaml."
    assert "cost" in content, \
        "Expected 'cost' field in initial inconvo.yaml."


def test_inconvo_yaml_does_not_yet_contain_gross_margin():
    yaml_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    with open(yaml_path, "r") as f:
        content = f.read()

    assert "gross_margin" not in content, \
        "Initial inconvo.yaml must NOT yet contain 'gross_margin'; the agent should add it."
