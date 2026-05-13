import os
import pytest

PROJECT_DIR = "/home/user/app"

def test_passwords_state_is_off():
    yaml_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    assert os.path.isfile(yaml_path), f"Semantic model file {yaml_path} does not exist."
    
    with open(yaml_path, "r") as f:
        lines = f.readlines()
        
    in_passwords = False
    passwords_state_off = False
    
    for line in lines:
        # Check indentation to know when we leave the passwords block
        if line.startswith("  passwords:"):
            in_passwords = True
        elif in_passwords and line.startswith("  ") and not line.startswith("    "):
            # If we hit another table level, we exit passwords
            if "passwords" not in line:
                in_passwords = False
                
        if in_passwords and "state:" in line:
            if "Off" in line:
                passwords_state_off = True
            break
            
    assert passwords_state_off, "The 'passwords' table must have 'state: Off' in inconvo.yaml."

def test_users_state_is_queryable():
    yaml_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    
    with open(yaml_path, "r") as f:
        lines = f.readlines()
        
    in_users = False
    users_state_queryable = False
    
    for line in lines:
        if line.startswith("  users:"):
            in_users = True
        elif in_users and line.startswith("  ") and not line.startswith("    "):
            if "users" not in line:
                in_users = False
                
        if in_users and "state:" in line:
            if "Queryable" in line:
                users_state_queryable = True
            break
            
    assert users_state_queryable, "The 'users' table must retain 'state: Queryable' in inconvo.yaml."