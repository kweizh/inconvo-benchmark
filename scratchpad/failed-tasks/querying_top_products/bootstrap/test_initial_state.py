import os
import yaml
import psycopg2

def test_project_exists():
    assert os.path.exists("/home/user/project")
    assert os.path.isdir("/home/user/project")

def test_inconvo_yaml_exists():
    yaml_path = "/home/user/project/inconvo.yaml"
    assert os.path.exists(yaml_path)
    with open(yaml_path, 'r') as f:
        config = yaml.safe_load(f)
    assert 'tables' in config

def test_database_connection():
    db_url = os.environ.get("DATABASE_URL")
    assert db_url is not None
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    cur.execute("SELECT 1")
    assert cur.fetchone()[0] == 1
    cur.close()
    conn.close()

def test_tables_exist():
    db_url = os.environ.get("DATABASE_URL")
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    tables = [row[0] for row in cur.fetchall()]
    assert 'products' in tables
    assert 'line_items' in tables
    cur.close()
    conn.close()

def test_initial_yaml_state():
    yaml_path = "/home/user/project/inconvo.yaml"
    with open(yaml_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Check that tables are initially Off or not fully configured
    products = config.get('tables', {}).get('products', {})
    assert products.get('state') == 'Off'
    
    line_items = config.get('tables', {}).get('line_items', {})
    assert line_items.get('state') == 'Off'
    
    assert not config.get('relations')
