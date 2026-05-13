import os
import json
import shutil
import pytest

PROJECT_DIR = "/home/user/app"
COMPONENT_PATH = os.path.join(
    PROJECT_DIR, "app", "components", "inconvo", "InconvoTableGrid.tsx"
)
CHAT_ROUTE_PATH = os.path.join(PROJECT_DIR, "app", "api", "chat", "route.ts")
PAGE_PATH = os.path.join(PROJECT_DIR, "app", "page.tsx")
PACKAGE_JSON_PATH = os.path.join(PROJECT_DIR, "package.json")
NODE_MODULES_PATH = os.path.join(PROJECT_DIR, "node_modules")


def test_node_available():
    assert shutil.which("node") is not None, "node binary not found in PATH."
    assert shutil.which("npm") is not None, "npm binary not found in PATH."


def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."


def test_chat_route_exists():
    assert os.path.isfile(CHAT_ROUTE_PATH), (
        f"Expected pre-existing chat API route at {CHAT_ROUTE_PATH}."
    )


def test_page_exists():
    assert os.path.isfile(PAGE_PATH), (
        f"Expected pre-existing app/page.tsx at {PAGE_PATH}."
    )


def test_table_grid_placeholder_exists():
    assert os.path.isfile(COMPONENT_PATH), (
        f"Expected placeholder InconvoTableGrid.tsx at {COMPONENT_PATH}."
    )


def test_table_grid_is_placeholder():
    with open(COMPONENT_PATH, "r") as f:
        content = f.read()
    assert "<table" not in content, (
        f"InconvoTableGrid.tsx must start as a placeholder without a <table> element. "
        f"Found <table in {COMPONENT_PATH}."
    )
    assert "<thead" not in content, (
        f"InconvoTableGrid.tsx must start as a placeholder without rendering logic. "
        f"Found <thead in {COMPONENT_PATH}."
    )
    assert "<tbody" not in content, (
        f"InconvoTableGrid.tsx must start as a placeholder without rendering logic. "
        f"Found <tbody in {COMPONENT_PATH}."
    )


def test_package_json_dependencies():
    assert os.path.isfile(PACKAGE_JSON_PATH), (
        f"package.json not found at {PACKAGE_JSON_PATH}."
    )
    with open(PACKAGE_JSON_PATH, "r") as f:
        data = json.load(f)
    deps = data.get("dependencies", {})
    assert "@inconvoai/vercel-ai-sdk" in deps, (
        "@inconvoai/vercel-ai-sdk must be listed in package.json dependencies."
    )
    assert "ai" in deps, "ai package must be listed in package.json dependencies."
    assert "next" in deps, "next must be listed in package.json dependencies."
    assert "react" in deps, "react must be listed in package.json dependencies."


def test_node_modules_installed():
    assert os.path.isdir(NODE_MODULES_PATH), (
        f"node_modules must be pre-installed at {NODE_MODULES_PATH}."
    )
    inconvo_pkg = os.path.join(NODE_MODULES_PATH, "@inconvoai", "vercel-ai-sdk")
    assert os.path.isdir(inconvo_pkg), (
        f"@inconvoai/vercel-ai-sdk must be installed at {inconvo_pkg}."
    )
