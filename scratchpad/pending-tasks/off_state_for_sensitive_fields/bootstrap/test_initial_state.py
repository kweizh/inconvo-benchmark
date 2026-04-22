import os
import yaml
import pytest

def test_initial_state():
    # Check if .inconvo directory exists
    assert os.path.exists(".inconvo"), ".inconvo directory should exist"
    
    # Check if inconvo.yaml exists (assuming it's in .inconvo/ or project root)
    model_path = ".inconvo/inconvo.yaml"
    assert os.path.exists(model_path), f"{model_path} should exist"
    
    with open(model_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Check that users table exists and is Queryable
    tables = config.get('tables', {})
    assert 'users' in tables, "users table should be in the semantic model"
    assert tables['users'].get('state') == 'Queryable', "users table should be Queryable initially"
    
    # Check that sensitive fields are currently On (or not Off)
    fields = tables['users'].get('fields', {})
    assert fields.get('password_hash', {}).get('state') != 'Off', "password_hash should not be Off initially"
    assert fields.get('secret_key', {}).get('state') != 'Off', "secret_key should not be Off initially"

if __name__ == "__main__":
    pytest.main([__file__])
