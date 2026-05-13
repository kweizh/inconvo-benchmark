import os
import shutil
import json
import pytest

PROJECT_DIR = "/home/user/app"
CHART_COMPONENT = os.path.join(
    PROJECT_DIR, "app/components/inconvo/InconvoChart.tsx"
)
PAGE_FILE = os.path.join(PROJECT_DIR, "app/page.tsx")
API_ROUTE_FILE = os.path.join(PROJECT_DIR, "app/api/chat/route.ts")


def test_node_available():
    assert shutil.which("node") is not None, "node binary not found in PATH."
    assert shutil.which("npm") is not None, "npm binary not found in PATH."


def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), (
        f"Project directory {PROJECT_DIR} does not exist."
    )


def test_package_json_declares_required_deps():
    pkg_path = os.path.join(PROJECT_DIR, "package.json")
    assert os.path.isfile(pkg_path), f"package.json not found at {pkg_path}"
    with open(pkg_path, "r") as f:
        data = json.load(f)
    deps = data.get("dependencies", {})
    assert "@inconvoai/vercel-ai-sdk" in deps, (
        "@inconvoai/vercel-ai-sdk should be declared in package.json dependencies."
    )
    assert "ai" in deps, "ai package should be declared in package.json dependencies."
    assert "next" in deps, "next should be declared in package.json dependencies."
    assert "react" in deps, "react should be declared in package.json dependencies."
    assert "recharts" in deps, (
        "recharts should be declared in package.json dependencies."
    )


def test_recharts_installed_in_node_modules():
    recharts_dir = os.path.join(PROJECT_DIR, "node_modules", "recharts")
    assert os.path.isdir(recharts_dir), (
        f"recharts is not installed in node_modules at {recharts_dir}."
    )


def test_inconvo_vercel_sdk_installed_in_node_modules():
    sdk_dir = os.path.join(
        PROJECT_DIR, "node_modules", "@inconvoai", "vercel-ai-sdk"
    )
    assert os.path.isdir(sdk_dir), (
        f"@inconvoai/vercel-ai-sdk is not installed in node_modules at {sdk_dir}."
    )


def test_api_route_exists():
    assert os.path.isfile(API_ROUTE_FILE), (
        f"Expected pre-existing API route at {API_ROUTE_FILE}."
    )


def test_page_file_exists():
    assert os.path.isfile(PAGE_FILE), (
        f"Expected pre-existing page file at {PAGE_FILE}."
    )


def test_chart_component_placeholder_exists():
    assert os.path.isfile(CHART_COMPONENT), (
        f"Expected placeholder chart component at {CHART_COMPONENT}."
    )


def test_chart_component_is_not_yet_implemented():
    with open(CHART_COMPONENT, "r") as f:
        content = f.read()
    assert "recharts" not in content, (
        "InconvoChart.tsx should not import 'recharts' yet — it is a placeholder."
    )
    assert "BarChart" not in content, (
        "InconvoChart.tsx should not reference 'BarChart' yet — it is a placeholder."
    )
