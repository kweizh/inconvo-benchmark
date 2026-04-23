import os
import yaml
import pytest

def test_inconvo_yaml_exists():
    path = "/home/user/inconvo-project/inconvo.yaml"
    assert os.path.exists(path), f"{path} does not exist"

def test_inconvo_yaml_content():
    path = "/home/user/inconvo-project/inconvo.yaml"
    with open(path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Check tables
    tables = config.get('tables', {})
    assert 'orders' in tables, "Table 'orders' not defined in inconvo.yaml"
    assert tables['orders'].get('state') == 'Queryable', "Table 'orders' should be Queryable"
    
    assert 'addresses' in tables, "Table 'addresses' not defined in inconvo.yaml"
    assert tables['addresses'].get('state') == 'Joinable', "Table 'addresses' should be Joinable"
    
    # Check relations
    relations = config.get('relations', [])
    assert len(relations) > 0, "No relations defined in inconvo.yaml"
    
    # Find the specific relation
    shipping_relation = next((r for r in relations if r.get('name') == 'order_to_shipping_address'), None)
    assert shipping_relation is not None, "Relation 'order_to_shipping_address' not found"
    
    assert shipping_relation.get('left') == 'orders.shipping_address_id', "Wrong left field for shipping relation"
    assert shipping_relation.get('right') == 'addresses.id', "Wrong right field for shipping relation"
    
    # Ensure billing relation is NOT there
    billing_relation = next((r for r in relations if 'billing_address_id' in str(r)), None)
    assert billing_relation is None, "Relation for 'billing_address_id' should not be defined"

def test_no_other_shipping_relations():
    path = "/home/user/inconvo-project/inconvo.yaml"
    with open(path, 'r') as f:
        config = yaml.safe_load(f)
    
    relations = config.get('relations', [])
    # Filter for relations involving orders and addresses
    related = [r for r in relations if ('orders' in str(r) and 'addresses' in str(r))]
    
    # Should only have one (the shipping one)
    assert len(related) == 1, f"Expected exactly 1 relation between orders and addresses, found {len(related)}"
