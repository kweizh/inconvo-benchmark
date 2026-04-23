import os
import pytest
import yaml

PROJECT_DIR = "/home/user/healthcare-agent"

def test_yaml_file_exists():
    yaml_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    assert os.path.isfile(yaml_path), f"inconvo.yaml not found at {yaml_path}"

def test_yaml_content_valid():
    yaml_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    with open(yaml_path, 'r') as f:
        content = yaml.safe_load(f)
    
    assert "tables" in content, "Expected 'tables' in inconvo.yaml"
    tables = content["tables"]
    
    assert "patients" in tables, "Expected 'patients' table"
    assert tables["patients"].get("state") == "Queryable", "Expected 'patients' state to be 'Queryable'"
    assert "fields" in tables["patients"], "Expected 'fields' in 'patients' table"
    assert tables["patients"]["fields"].get("id", {}).get("state") == "On", "Expected 'id' field in 'patients' to be 'On'"
    assert tables["patients"]["fields"].get("birth_date", {}).get("state") == "On", "Expected 'birth_date' field in 'patients' to be 'On'"
    
    assert "encounters" in tables, "Expected 'encounters' table"
    assert tables["encounters"].get("state") == "Queryable", "Expected 'encounters' state to be 'Queryable'"
    assert "fields" in tables["encounters"], "Expected 'fields' in 'encounters' table"
    assert tables["encounters"]["fields"].get("total_cost", {}).get("state") == "On", "Expected 'total_cost' field in 'encounters' to be 'On'"
    assert tables["encounters"]["fields"].get("total_cost", {}).get("type") == "measure", "Expected 'total_cost' type to be 'measure'"
    
    assert "practitioners" in tables, "Expected 'practitioners' table"
    assert tables["practitioners"].get("state") == "Joinable", "Expected 'practitioners' state to be 'Joinable'"
    
    assert "relations" in content, "Expected 'relations' in inconvo.yaml"
    relations = content["relations"]
    
    patient_encounters = next((r for r in relations if r.get("name") == "patient_encounters"), None)
    assert patient_encounters is not None, "Expected relation 'patient_encounters'"
    assert patient_encounters.get("left") == "encounters.patient_id", "Expected left to be 'encounters.patient_id'"
    assert patient_encounters.get("right") == "patients.id", "Expected right to be 'patients.id'"
    
    practitioner_encounters = next((r for r in relations if r.get("name") == "practitioner_encounters"), None)
    assert practitioner_encounters is not None, "Expected relation 'practitioner_encounters'"
    assert practitioner_encounters.get("left") == "encounters.practitioner_id", "Expected left to be 'encounters.practitioner_id'"
    assert practitioner_encounters.get("right") == "practitioners.id", "Expected right to be 'practitioners.id'"
