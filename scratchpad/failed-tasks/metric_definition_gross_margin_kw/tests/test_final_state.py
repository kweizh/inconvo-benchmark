import os
import yaml

def test_final_state():
    yaml_path = '/home/user/myproject/inconvo.yaml'
    assert os.path.exists(yaml_path), "inconvo.yaml must exist"
    
    with open(yaml_path, 'r') as f:
        config = yaml.safe_load(f)
        
    orders_table = config.get('tables', {}).get('orders', {})
    fields = orders_table.get('fields', {})
    
    assert 'gross_margin' in fields, "gross_margin field is missing"
    
    gross_margin_field = fields['gross_margin']
    
    # Check properties
    assert gross_margin_field.get('state') == 'On', "state must be On"
    assert gross_margin_field.get('type') == 'measure', "type must be measure"
    
    # Check expression
    expr = gross_margin_field.get('expression', '')
    if not expr:
        expr = gross_margin_field.get('sql', '')
        
    assert 'revenue' in expr and 'cost' in expr and '-' in expr, f"Expression is incorrect: {expr}"
