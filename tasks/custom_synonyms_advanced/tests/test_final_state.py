import os
import pytest
import yaml

CONFIG_FILE = "/home/user/project/inconvo.yaml"

def test_config_file_exists():
    assert os.path.isfile(CONFIG_FILE), f"Config file {CONFIG_FILE} does not exist."

def test_synonyms_configured():
    with open(CONFIG_FILE, 'r') as f:
        try:
            config = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            pytest.fail(f"Invalid YAML in inconvo.yaml: {exc}")
    
    # Check orders.total_amount synonyms
    try:
        total_amount_field = config['tables']['orders']['fields']['total_amount']
    except KeyError:
        pytest.fail("Field 'total_amount' in table 'orders' is missing or malformed.")
        
    assert 'synonyms' in total_amount_field, "Expected 'synonyms' key in 'total_amount' field."
    synonyms = total_amount_field['synonyms']
    assert isinstance(synonyms, list), "Expected 'synonyms' to be a list."
    assert 'revenue' in synonyms, "Expected 'revenue' in 'total_amount' synonyms."
    assert 'gross_sales' in synonyms, "Expected 'gross_sales' in 'total_amount' synonyms."
    
    # Check customers.name synonyms
    try:
        name_field = config['tables']['customers']['fields']['name']
    except KeyError:
        pytest.fail("Field 'name' in table 'customers' is missing or malformed.")
        
    assert 'synonyms' in name_field, "Expected 'synonyms' key in 'name' field."
    synonyms = name_field['synonyms']
    assert isinstance(synonyms, list), "Expected 'synonyms' to be a list."
    assert 'client_name' in synonyms, "Expected 'client_name' in 'name' synonyms."
