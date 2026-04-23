import os
import pytest
import yaml

PROJECT_DIR = "/home/user/myproject"

def test_customers_table_is_queryable():
    model_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    with open(model_path) as f:
        data = yaml.safe_load(f)
    
    assert "customers" in data.get("tables", {}), "Expected 'customers' table in inconvo.yaml."
    assert data["tables"]["customers"].get("state") == "Queryable", \
        "Expected 'customers' table to have state 'Queryable'."

def test_full_name_field_is_on_and_dimension():
    model_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    with open(model_path) as f:
        data = yaml.safe_load(f)
    
    fields = data.get("tables", {}).get("customers", {}).get("fields", {})
    assert "full_name" in fields, "Expected 'full_name' field under customers in inconvo.yaml."
    
    assert fields["full_name"].get("state") == "On", \
        "Expected 'full_name' field to have state 'On'."
    assert fields["full_name"].get("type") == "dimension", \
        "Expected 'full_name' field to have type 'dimension'."

def test_full_name_field_has_synonyms():
    model_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    with open(model_path) as f:
        data = yaml.safe_load(f)
    
    synonyms = data.get("tables", {}).get("customers", {}).get("fields", {}).get("full_name", {}).get("synonyms", [])
    assert isinstance(synonyms, list), "Expected 'synonyms' to be a list."
    assert "client name" in synonyms, "Expected 'client name' synonym in inconvo.yaml."
    assert "purchaser" in synonyms, "Expected 'purchaser' synonym in inconvo.yaml."

def test_env_file_has_database_url():
    env_path = os.path.join(PROJECT_DIR, ".env")
    assert os.path.isfile(env_path), f"Expected .env file at {env_path}"
    with open(env_path) as f:
        content = f.read()
    assert "DATABASE_URL=" in content, "Expected DATABASE_URL in .env file."
