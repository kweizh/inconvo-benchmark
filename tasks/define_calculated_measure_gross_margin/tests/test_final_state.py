import os
import yaml
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_gross_margin_computed_column_exists():
    config_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    assert os.path.isfile(config_path), f"Config file {config_path} does not exist."
    
    with open(config_path) as f:
        content = yaml.safe_load(f)
        
    products_table = content.get("tables", {}).get("products", {})
    assert products_table, "The 'products' table is missing."
    
    fields = products_table.get("fields", {})
    assert "gross_margin" in fields, "The 'gross_margin' field is missing from the 'products' table."
    
    gross_margin = fields["gross_margin"]
    assert gross_margin.get("type") == "measure", "The 'gross_margin' field must have type: measure."
    assert gross_margin.get("unit") == "%", "The 'gross_margin' field must have unit: %."
    assert "expression" in gross_margin, "The 'gross_margin' field must have an expression."
    expression = gross_margin.get("expression", "").replace(" ", "")
    assert expression == "(price-cost)/price*100", "The expression is incorrect."
