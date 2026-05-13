import os
import shutil
import pytest

PROJECT_DIR = "/home/user/inconvo-app"
YAML_FILE = os.path.join(PROJECT_DIR, "inconvo.yaml")
INDEX_JS = os.path.join(PROJECT_DIR, "index.js")
SDK_DIR = os.path.join(PROJECT_DIR, "node_modules", "@inconvoai", "node")


def test_node_installed():
    assert shutil.which("node") is not None, "node binary not found in PATH."
    assert shutil.which("npm") is not None, "npm binary not found in PATH."


def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."


def test_inconvo_yaml_exists():
    assert os.path.isfile(YAML_FILE), f"Config file {YAML_FILE} does not exist."


def test_inconvo_yaml_declares_line_items_and_products():
    with open(YAML_FILE, "r") as f:
        content = f.read()
    assert "line_items" in content, "Expected 'line_items' table to be present in inconvo.yaml."
    assert "products" in content, "Expected 'products' table to be present in inconvo.yaml."


def test_inconvo_yaml_has_no_line_item_to_product_relation():
    with open(YAML_FILE, "r") as f:
        content = f.read()
    assert "line_item_to_product" not in content, (
        "inconvo.yaml must NOT yet contain the 'line_item_to_product' relation; "
        "the agent is expected to add it."
    )


def test_inconvoai_node_sdk_installed():
    assert os.path.isdir(SDK_DIR), (
        f"Expected @inconvoai/node SDK to be installed under {SDK_DIR}."
    )


def test_index_js_exists():
    assert os.path.isfile(INDEX_JS), f"index.js not found at {INDEX_JS}."
