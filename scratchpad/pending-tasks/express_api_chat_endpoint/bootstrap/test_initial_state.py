import json
import os
import shutil
import pytest

PROJECT_DIR = "/home/user/inconvo-app"


def test_node_available():
    assert shutil.which("node") is not None, "node binary not found in PATH."


def test_npm_available():
    assert shutil.which("npm") is not None, "npm binary not found in PATH."


def test_project_directory_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."


def test_package_json_exists_and_lists_required_dependencies():
    package_json_path = os.path.join(PROJECT_DIR, "package.json")
    assert os.path.isfile(package_json_path), (
        f"package.json not found at {package_json_path}"
    )

    with open(package_json_path, "r") as f:
        data = json.load(f)

    deps = {}
    deps.update(data.get("dependencies", {}) or {})
    deps.update(data.get("devDependencies", {}) or {})

    assert "express" in deps, (
        f"Expected 'express' to be declared in package.json dependencies, got: {sorted(deps)}"
    )
    assert "@inconvoai/node" in deps, (
        f"Expected '@inconvoai/node' to be declared in package.json dependencies, got: {sorted(deps)}"
    )
    assert "dotenv" in deps, (
        f"Expected 'dotenv' to be declared in package.json dependencies, got: {sorted(deps)}"
    )


def test_node_modules_express_installed():
    express_dir = os.path.join(PROJECT_DIR, "node_modules", "express")
    assert os.path.isdir(express_dir), (
        f"express package not installed at {express_dir}. node_modules should be pre-installed."
    )


def test_node_modules_inconvo_installed():
    inconvo_dir = os.path.join(PROJECT_DIR, "node_modules", "@inconvoai", "node")
    assert os.path.isdir(inconvo_dir), (
        f"@inconvoai/node package not installed at {inconvo_dir}. node_modules should be pre-installed."
    )


def test_inconvo_yaml_starter_present():
    yaml_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    assert os.path.isfile(yaml_path), (
        f"Starter inconvo.yaml not found at {yaml_path}."
    )
