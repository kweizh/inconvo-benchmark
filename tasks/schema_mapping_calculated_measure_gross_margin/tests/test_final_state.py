import os
import pytest

PROJECT_DIR = "/home/user/inconvo-app"
YAML_FILE = os.path.join(PROJECT_DIR, "inconvo.yaml")

def test_gross_margin_field_exists():
    assert os.path.isfile(YAML_FILE), f"inconvo.yaml not found at {YAML_FILE}"
    
    with open(YAML_FILE, "r") as f:
        content = f.read()
        
    assert "gross_margin:" in content, "Expected 'gross_margin' field to be added to inconvo.yaml"

def test_gross_margin_is_measure_and_has_formula():
    with open(YAML_FILE, "r") as f:
        content = f.read().lower()
        
    # Since we can't use pyyaml, we will do a broader check
    # We want to ensure that "measure" and "revenue" and "cost" and "-" appear after "gross_margin:"
    # This is a bit loose but works for verifying the LLM's output
    assert "gross_margin:" in content, "Could not find gross_margin line"
    
    parts = content.split("gross_margin:")
    after_gross_margin = parts[1]
    
    # We only look at the first few lines after gross_margin:
    lines_after = after_gross_margin.split('\n')[:5]
    block = " ".join(lines_after)
    
    assert "measure" in block, f"Expected 'gross_margin' to have type 'measure', found in block: {block}"
    assert "revenue" in block and "cost" in block and "-" in block, \
        f"Expected 'gross_margin' to compute 'revenue - cost', found in block: {block}"
