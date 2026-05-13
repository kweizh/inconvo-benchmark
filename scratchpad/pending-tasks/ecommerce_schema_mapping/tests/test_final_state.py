import os
import subprocess
import yaml
import pytest

PROJECT_DIR = "/home/user/ecommerce-agent"
YAML_FILE = os.path.join(PROJECT_DIR, "inconvo.yaml")

def test_yaml_file_exists():
    assert os.path.isfile(YAML_FILE), f"inconvo.yaml not found at {YAML_FILE}"

def test_yaml_content():
    with open(YAML_FILE, "r") as f:
        data = yaml.safe_load(f)
        
    assert "tables" in data, "Expected 'tables' key in inconvo.yaml"
    tables = data["tables"]
    
    assert "users" in tables, "Expected 'users' table in inconvo.yaml"
    assert tables["users"].get("state") == "Queryable", "users table must be Queryable"
    users_fields = tables["users"].get("fields", {})
    assert users_fields.get("id", {}).get("state") == "On", "users.id must be On"
    assert users_fields.get("email", {}).get("state") == "On", "users.email must be On"
    for field, config in users_fields.items():
        if field not in ["id", "email"]:
            assert config.get("state") != "On", f"users.{field} should not be On"
            
    assert "products" in tables, "Expected 'products' table in inconvo.yaml"
    assert tables["products"].get("state") == "Queryable", "products table must be Queryable"
    products_fields = tables["products"].get("fields", {})
    assert products_fields.get("id", {}).get("state") == "On", "products.id must be On"
    assert products_fields.get("name", {}).get("state") == "On", "products.name must be On"
    assert products_fields.get("price", {}).get("state") == "On", "products.price must be On"
    for field, config in products_fields.items():
        if field not in ["id", "name", "price"]:
            assert config.get("state") != "On", f"products.{field} should not be On"
            
    assert "orders" in tables, "Expected 'orders' table in inconvo.yaml"
    assert tables["orders"].get("state") == "Queryable", "orders table must be Queryable"
    orders_fields = tables["orders"].get("fields", {})
    assert orders_fields.get("id", {}).get("state") == "On", "orders.id must be On"
    assert orders_fields.get("user_id", {}).get("state") == "On", "orders.user_id must be On"
    assert orders_fields.get("product_id", {}).get("state") == "On", "orders.product_id must be On"
    assert orders_fields.get("quantity", {}).get("state") == "On", "orders.quantity must be On"
    for field, config in orders_fields.items():
        if field not in ["id", "user_id", "product_id", "quantity"]:
            assert config.get("state") != "On", f"orders.{field} should not be On"
            
    assert "relations" in data, "Expected 'relations' key in inconvo.yaml"
    relations = data["relations"]
    
    order_to_user = next((r for r in relations if r.get("name") == "order_to_user"), None)
    assert order_to_user is not None, "Expected relation 'order_to_user'"
    assert order_to_user.get("left") == "orders.user_id", "order_to_user left must be orders.user_id"
    assert order_to_user.get("right") == "users.id", "order_to_user right must be users.id"
    
    order_to_product = next((r for r in relations if r.get("name") == "order_to_product"), None)
    assert order_to_product is not None, "Expected relation 'order_to_product'"
    assert order_to_product.get("left") == "orders.product_id", "order_to_product left must be orders.product_id"
    assert order_to_product.get("right") == "products.id", "order_to_product right must be products.id"

def test_inconvo_model_push():
    env = os.environ.copy()
    assert "INCONVO_AGENT_ID" in env, "INCONVO_AGENT_ID not set"
    assert "INCONVO_API_KEY" in env, "INCONVO_API_KEY not set"
    
    # Run inconvo model push to validate
    # Note: Using npx inconvo@latest to ensure it runs
    result = subprocess.run(
        ["npx", "inconvo@latest", "model", "push"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        env=env
    )
    
    assert result.returncode == 0, f"inconvo model push failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
