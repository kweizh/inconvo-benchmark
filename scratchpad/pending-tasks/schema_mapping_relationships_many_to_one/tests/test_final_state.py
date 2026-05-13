import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/inconvo-app"

def test_relations_in_yaml():
    yaml_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    assert os.path.isfile(yaml_path), f"Config file {yaml_path} does not exist."
    with open(yaml_path, "r") as f:
        content = f.read()
    assert "relations:" in content, "Expected 'relations:' section in inconvo.yaml."
    assert "line_item_to_product" in content, "Expected relationship 'line_item_to_product' in inconvo.yaml."
    assert "line_items.product_id" in content, "Expected 'line_items.product_id' in relationship."
    assert "products.id" in content, "Expected 'products.id' in relationship."

def test_node_index_js_success():
    result = subprocess.run(
        ["node", "index.js"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"'node index.js' failed with output: {result.stderr}\n{result.stdout}"
