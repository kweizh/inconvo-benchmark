import os
import yaml
import pytest

PROJECT_DIR = "/home/user/ecommerce-agent"
YAML_FILE = os.path.join(PROJECT_DIR, "inconvo.yaml")

def test_inconvo_yaml_exists():
    assert os.path.isfile(YAML_FILE), f"inconvo.yaml not found at {YAML_FILE}"

def test_inconvo_yaml_content():
    with open(YAML_FILE, "r") as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            pytest.fail(f"inconvo.yaml is not valid YAML: {e}")

    assert "tables" in data, "Expected 'tables' block in inconvo.yaml"
    tables = data["tables"]
    
    # Check orders
    assert "orders" in tables, "Expected 'orders' table in inconvo.yaml"
    assert tables["orders"].get("state") == "Queryable", "Expected 'orders' state to be 'Queryable'"
    assert "fields" in tables["orders"], "Expected 'fields' in 'orders' table"
    order_fields = tables["orders"]["fields"]
    assert "id" in order_fields and order_fields["id"].get("state") == "On", "Expected 'id' field in 'orders' with state 'On'"
    assert "total_amount" in order_fields and order_fields["total_amount"].get("state") == "On", "Expected 'total_amount' field in 'orders' with state 'On'"
    assert order_fields["total_amount"].get("type") == "measure", "Expected 'total_amount' field in 'orders' to be type 'measure'"
    assert "user_id" in order_fields and order_fields["user_id"].get("state") == "On", "Expected 'user_id' field in 'orders' with state 'On'"

    # Check products
    assert "products" in tables, "Expected 'products' table in inconvo.yaml"
    assert tables["products"].get("state") == "Queryable", "Expected 'products' state to be 'Queryable'"
    assert "fields" in tables["products"], "Expected 'fields' in 'products' table"
    product_fields = tables["products"]["fields"]
    assert "id" in product_fields and product_fields["id"].get("state") == "On", "Expected 'id' field in 'products' with state 'On'"
    assert "name" in product_fields and product_fields["name"].get("state") == "On", "Expected 'name' field in 'products' with state 'On'"
    assert "price" in product_fields and product_fields["price"].get("state") == "On", "Expected 'price' field in 'products' with state 'On'"
    assert product_fields["price"].get("type") == "measure", "Expected 'price' field in 'products' to be type 'measure'"

    # Check users
    assert "users" in tables, "Expected 'users' table in inconvo.yaml"
    assert tables["users"].get("state") == "Joinable", "Expected 'users' state to be 'Joinable'"
    assert "fields" in tables["users"], "Expected 'fields' in 'users' table"
    user_fields = tables["users"]["fields"]
    assert "id" in user_fields and user_fields["id"].get("state") == "On", "Expected 'id' field in 'users' with state 'On'"
    assert "email" in user_fields and user_fields["email"].get("state") == "On", "Expected 'email' field in 'users' with state 'On'"

    # Check relations
    assert "relations" in data, "Expected 'relations' block in inconvo.yaml"
    relations = data["relations"]
    assert any(r.get("name") == "order_to_user" and r.get("left") == "orders.user_id" and r.get("right") == "users.id" for r in relations), \
        "Expected relation 'order_to_user' mapping 'orders.user_id' to 'users.id'"
