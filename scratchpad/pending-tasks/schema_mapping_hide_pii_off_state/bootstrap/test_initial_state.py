import os
import shutil
import pytest

PROJECT_DIR = "/home/user/inconvo-app"
YAML_FILE = os.path.join(PROJECT_DIR, "inconvo.yaml")
NODE_MODULES_SDK = os.path.join(PROJECT_DIR, "node_modules", "@inconvoai", "node")


def test_node_available():
    assert shutil.which("node") is not None, "node binary not found in PATH."
    assert shutil.which("npm") is not None, "npm binary not found in PATH."


def test_project_directory_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."


def test_inconvo_yaml_exists():
    assert os.path.isfile(YAML_FILE), f"Config file {YAML_FILE} does not exist."


def test_inconvo_yaml_initial_pii_state_is_on():
    with open(YAML_FILE, "r") as f:
        content = f.read()
    assert "customers" in content, "Expected 'customers' table definition in inconvo.yaml."
    assert "email" in content, "Expected 'email' field under customers in inconvo.yaml."
    assert "phone" in content, "Expected 'phone' field under customers in inconvo.yaml."

    # The PII fields must NOT already be set to Off — the task is to flip them.
    parts = content.split("email:")
    assert len(parts) >= 2, "Expected 'email:' field declaration in inconvo.yaml."
    email_block = parts[1].split("\n", 1)[0]
    assert "Off" not in email_block, (
        "Expected initial state of customers.email to be 'On', "
        f"but the inline block already contains 'Off': {email_block}"
    )

    parts_phone = content.split("phone:")
    assert len(parts_phone) >= 2, "Expected 'phone:' field declaration in inconvo.yaml."
    phone_block = parts_phone[1].split("\n", 1)[0]
    assert "Off" not in phone_block, (
        "Expected initial state of customers.phone to be 'On', "
        f"but the inline block already contains 'Off': {phone_block}"
    )


def test_inconvoai_node_sdk_installed():
    assert os.path.isdir(NODE_MODULES_SDK), (
        f"Expected @inconvoai/node SDK to be pre-installed at {NODE_MODULES_SDK}."
    )
