import os
import yaml
import psycopg2

def test_inconvo_yaml_configured():
    yaml_path = "/home/user/project/inconvo.yaml"
    assert os.path.exists(yaml_path)
    with open(yaml_path, 'r') as f:
        config = yaml.safe_load(f)
    
    tables = config.get('tables', {})
    
    # Check products table
    products = tables.get('products', {})
    assert products.get('state') == 'Queryable'
    product_fields = products.get('fields', {})
    assert product_fields.get('id', {}).get('state') == 'On'
    assert product_fields.get('name', {}).get('state') == 'On'
    
    # Check line_items table
    line_items = tables.get('line_items', {})
    assert line_items.get('state') == 'Queryable'
    line_item_fields = line_items.get('fields', {})
    assert line_item_fields.get('id', {}).get('state') == 'On'
    assert line_item_fields.get('product_id', {}).get('state') == 'On'
    assert line_item_fields.get('quantity', {}).get('state') == 'On'
    assert line_item_fields.get('quantity', {}).get('type') == 'measure'

def test_relationship_defined():
    yaml_path = "/home/user/project/inconvo.yaml"
    with open(yaml_path, 'r') as f:
        config = yaml.safe_load(f)
    
    relations = config.get('relations', [])
    found = False
    for rel in relations:
        if rel.get('name') == 'line_item_to_product':
            assert rel.get('left') == 'line_items.product_id'
            assert rel.get('right') == 'products.id'
            found = True
            break
    assert found, "Relationship 'line_item_to_product' not found"

def test_database_remains_accessible():
    db_url = os.environ.get("DATABASE_URL")
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM products")
    assert cur.fetchone()[0] > 0
    cur.close()
    conn.close()
