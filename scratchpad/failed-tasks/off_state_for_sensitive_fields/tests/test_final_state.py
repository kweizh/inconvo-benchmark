import os
import yaml
import pytest

def test_inconvo_yaml_exists():
    assert os.path.exists("inconvo.yaml"), "inconvo.yaml was not created"

def test_table_states():
    with open("inconvo.yaml", "r") as f:
        config = yaml.safe_load(f)
    
    tables = config.get("tables", {})
    
    assert "orders" in tables, "orders table not found in inconvo.yaml"
    assert tables["orders"].get("state") == "Queryable", f"orders table state should be Queryable, got {tables['orders'].get('state')}"
    
    assert "customers" in tables, "customers table not found in inconvo.yaml"
    assert tables["customers"].get("state") == "Joinable", f"customers table state should be Joinable, got {tables['customers'].get('state')}"

def test_relations():
    with open("inconvo.yaml", "r") as f:
        config = yaml.safe_load(f)
    
    relations = config.get("relations", [])
    
    # Check if there's a relation between orders and customers
    found = False
    for rel in relations:
        left = rel.get("left", "")
        right = rel.get("right", "")
        if (left == "orders.customer_id" and right == "customers.id") or \
           (left == "customers.id" and right == "orders.customer_id"):
            found = True
            break
    
    assert found, "Relation between orders.customer_id and customers.id not found"
