import os
import yaml

PROJECT_DIR = "/home/user/myproject"

def test_synonyms_configured():
    config_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
        
    assert 'tables' in config, "The 'tables' key is missing in inconvo.yaml"
    assert 'users' in config['tables'], "The 'users' table is missing in inconvo.yaml"
    assert 'fields' in config['tables']['users'], "The 'users' table is missing the 'fields' key"
    
    fields = config['tables']['users']['fields']
    assert 'customer_name' in fields, "The 'customer_name' field is missing in the 'users' table"
    
    customer_name_field = fields['customer_name']
    assert 'synonyms' in customer_name_field, "The 'synonyms' key is missing in the 'customer_name' field"
    
    synonyms = customer_name_field['synonyms']
    assert isinstance(synonyms, list), f"Expected 'synonyms' to be a list, got {type(synonyms)}"
    assert 'client' in synonyms, f"Expected 'client' to be in synonyms, got {synonyms}"
    assert 'shopper' in synonyms, f"Expected 'shopper' to be in synonyms, got {synonyms}"
