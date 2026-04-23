import os
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_order_to_line_item_relation_configured():
    """Priority 3 fallback: Verify the order_to_line_item relation is in the YAML file."""
    config_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    with open(config_path) as f:
        content = f.read()
    
    assert "name: order_to_line_item" in content, "Expected relation 'order_to_line_item' in inconvo.yaml."
    assert "left: orders.id" in content, "Expected left side of 'order_to_line_item' to be 'orders.id'."
    assert "right: line_items.order_id" in content, "Expected right side of 'order_to_line_item' to be 'line_items.order_id'."

def test_line_item_to_product_relation_configured():
    """Priority 3 fallback: Verify the line_item_to_product relation is in the YAML file."""
    config_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    with open(config_path) as f:
        content = f.read()
    
    assert "name: line_item_to_product" in content, "Expected relation 'line_item_to_product' in inconvo.yaml."
    assert "left: line_items.product_id" in content, "Expected left side of 'line_item_to_product' to be 'line_items.product_id'."
    assert "right: products.id" in content, "Expected right side of 'line_item_to_product' to be 'products.id'."