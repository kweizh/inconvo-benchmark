import os
import yaml

def test_final_state():
    assert os.path.exists('/home/user/myproject/inconvo.yaml')
    with open('/home/user/myproject/inconvo.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    users_table = config.get('tables', {}).get('users', {})
    fields = users_table.get('fields', {})
    
    assert 'is_active' in fields, "is_active field is missing"
    
    is_active_field = fields['is_active']
    assert 'last_login > \\'2025-01-01\\'' in str(is_active_field) or 'sql' in is_active_field, "SQL expression is missing or incorrect"
    
    # Just check if it's there
    is_active_str = str(is_active_field).replace('"', "'")
    assert "last_login > '2025-01-01'" in is_active_str, f"Expression not found in {is_active_str}"
