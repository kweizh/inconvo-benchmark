import os

def test_final_state():
    # Check if .inconvo directory exists
    assert os.path.exists(".inconvo"), ".inconvo directory was not created"
    
    # Check for core configuration file
    assert os.path.exists(".inconvo/inconvo.yaml"), "inconvo.yaml was not created"
    
    # Optionally check if tables were synced (this depends on CLI behavior)
    # If inconvo model pull creates a tables directory:
    # assert os.path.exists(".inconvo/tables"), "tables directory was not created in .inconvo"
    
    with open(".inconvo/inconvo.yaml", "r") as f:
        content = f.read()
        # Verify that the schema from init_db.sql is reflected
        assert "users" in content.lower()
        assert "orders" in content.lower()
        assert "products" in content.lower()
