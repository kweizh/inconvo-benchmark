import os
import yaml
import pytest

def test_inconvo_yaml_exists():
    assert os.path.exists("inconvo.yaml")

def test_security_policy_configured():
    with open("inconvo.yaml", "r") as f:
        config = yaml.safe_load(f)
    
    # Check if sales table has a context filter
    # Based on docs: WHERE orders.organisation_id = userContext.organisationId;
    # The instruction says organisation_id for both.
    
    sales_table = config.get("tables", {}).get("sales", {})
    context_filter = sales_table.get("context_filter") or sales_table.get("filter")
    
    assert context_filter is not None, "Security policy (context filter) not found on sales table"
    assert "organisation_id" in context_filter
    assert "userContext.organisation_id" in context_filter
