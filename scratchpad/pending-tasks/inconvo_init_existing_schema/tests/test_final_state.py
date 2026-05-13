import os
import pathlib
import pytest

PROJECT_DIR = "/home/user/project"

def test_semantic_model_files_exist():
    # Check if inconvo.yaml exists or .inconvo directory exists
    has_yaml = os.path.isfile(os.path.join(PROJECT_DIR, "inconvo.yaml"))
    has_dir = os.path.isdir(os.path.join(PROJECT_DIR, ".inconvo"))
    
    assert has_yaml or has_dir, "Inconvo semantic model configuration (inconvo.yaml or .inconvo/ directory) not found."

def test_tables_defined_in_model():
    # Search for table definitions in the configuration files
    found_users = False
    found_orders = False
    found_products = False
    
    # Files to check
    files_to_check = []
    if os.path.isfile(os.path.join(PROJECT_DIR, "inconvo.yaml")):
        files_to_check.append(os.path.join(PROJECT_DIR, "inconvo.yaml"))
        
    inconvo_dir = os.path.join(PROJECT_DIR, ".inconvo")
    if os.path.isdir(inconvo_dir):
        for root, _, files in os.walk(inconvo_dir):
            for file in files:
                if file.endswith(".yaml") or file.endswith(".yml") or file.endswith(".json"):
                    files_to_check.append(os.path.join(root, file))
                    
    assert len(files_to_check) > 0, "No configuration files found to check for tables."
    
    for file_path in files_to_check:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().lower()
            if "users" in content:
                found_users = True
            if "orders" in content:
                found_orders = True
            if "products" in content:
                found_products = True
                
    assert found_users, "Table 'users' definition not found in the semantic model."
    assert found_orders, "Table 'orders' definition not found in the semantic model."
    assert found_products, "Table 'products' definition not found in the semantic model."

def test_relationships_defined_in_model():
    # Search for relationships (foreign keys) in the configuration files
    found_user_order_rel = False
    found_product_order_rel = False
    
    files_to_check = []
    if os.path.isfile(os.path.join(PROJECT_DIR, "inconvo.yaml")):
        files_to_check.append(os.path.join(PROJECT_DIR, "inconvo.yaml"))
        
    inconvo_dir = os.path.join(PROJECT_DIR, ".inconvo")
    if os.path.isdir(inconvo_dir):
        for root, _, files in os.walk(inconvo_dir):
            for file in files:
                if file.endswith(".yaml") or file.endswith(".yml") or file.endswith(".json"):
                    files_to_check.append(os.path.join(root, file))
                    
    for file_path in files_to_check:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().lower()
            # Look for indicators of relationships like "user_id", "product_id" or "relation"
            if "user_id" in content or "users.id" in content:
                found_user_order_rel = True
            if "product_id" in content or "products.id" in content:
                found_product_order_rel = True
                
    assert found_user_order_rel, "Relationship between users and orders (user_id) not found in the semantic model."
    assert found_product_order_rel, "Relationship between products and orders (product_id) not found in the semantic model."
