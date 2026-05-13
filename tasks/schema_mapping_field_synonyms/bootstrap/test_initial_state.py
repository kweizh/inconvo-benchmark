import os
import shutil
import pytest

PROJECT_DIR = "/home/user/inconvo-app"
INCONVO_YAML = os.path.join(PROJECT_DIR, "inconvo.yaml")
NODE_MODULES_INCONVO = os.path.join(PROJECT_DIR, "node_modules", "@inconvoai", "node")


def test_node_available():
    assert shutil.which("node") is not None, "node binary not found in PATH."
    assert shutil.which("npm") is not None, "npm binary not found in PATH."


def test_project_directory_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."


def test_package_json_exists():
    package_json = os.path.join(PROJECT_DIR, "package.json")
    assert os.path.isfile(package_json), f"package.json not found at {package_json}"


def test_inconvoai_node_installed():
    assert os.path.isdir(NODE_MODULES_INCONVO), (
        f"@inconvoai/node not pre-installed at {NODE_MODULES_INCONVO}"
    )


def test_dotenv_installed():
    dotenv_dir = os.path.join(PROJECT_DIR, "node_modules", "dotenv")
    assert os.path.isdir(dotenv_dir), f"dotenv not pre-installed at {dotenv_dir}"


def test_inconvo_yaml_exists():
    assert os.path.isfile(INCONVO_YAML), f"inconvo.yaml not found at {INCONVO_YAML}"


def test_inconvo_yaml_has_initial_tables():
    with open(INCONVO_YAML, "r") as f:
        content = f.read()
    assert "orders" in content, "Expected 'orders' table definition in inconvo.yaml"
    assert "customers" in content, "Expected 'customers' table definition in inconvo.yaml"
    assert "total_amount" in content, "Expected 'total_amount' field in inconvo.yaml"


def test_inconvo_yaml_has_no_synonyms_yet():
    with open(INCONVO_YAML, "r") as f:
        content = f.read().lower()
    assert "revenue" not in content, (
        "Did not expect 'revenue' synonym in inconvo.yaml before the task starts."
    )
    assert "buyer" not in content, (
        "Did not expect 'buyer' synonym in inconvo.yaml before the task starts."
    )
