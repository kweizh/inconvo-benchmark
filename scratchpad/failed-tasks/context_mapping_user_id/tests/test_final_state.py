import os
import yaml
import pytest

def test_inconvo_yaml_context_filter():
    assert os.path.exists("inconvo.yaml"), "inconvo.yaml is missing"
    
    with open("inconvo.yaml", "r") as f:
        config = yaml.safe_load(f)
    
    assert "tables" in config, "'tables' section missing in inconvo.yaml"
    assert "sales" in config["tables"], "'sales' table missing in 'tables' section"
    
    sales_config = config["tables"]["sales"]
    assert "contextFilters" in sales_config, "contextFilters missing for 'sales' table"
    
    filters = sales_config["contextFilters"]
    # We expect a mapping like:
    # contextFilters:
    #   organisation_id: organisation_id
    # OR if it's a list:
    # contextFilters:
    #   - column: organisation_id
    #     key: organisation_id
    
    found = False
    if isinstance(filters, dict):
        if "organisation_id" in filters and filters["organisation_id"] == "organisation_id":
            found = True
    elif isinstance(filters, list):
        for f in filters:
            if f.get("column") == "organisation_id" and f.get("key") == "organisation_id":
                found = True
                break
    
    assert found, "Context filter for 'organisation_id' mapping to 'organisation_id' not found in 'sales' table"

# Optional: verify it actually works by calling inconvo (mocked or real if possible)
# But typically static analysis of the config is enough for this level of task.
