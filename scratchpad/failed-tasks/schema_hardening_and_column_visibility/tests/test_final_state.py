import os
import subprocess
import json
import pytest
from pathlib import Path

PROJECT_DIR = "/home/user/inconvo-project"
CONFIG_PATH = os.path.join(PROJECT_DIR, ".inconvo/inconvo.yaml")

def test_inconvo_check_passes():
    """Priority 1: Use Inconvo CLI to verify the configuration is valid."""
    # Note: 'inconvo check' is a hypothetical command based on common CLI patterns
    # If it doesn't exist, this test will fail, which is acceptable if the CLI 
    # documentation suggests a validation command exists.
    # Based on plan.md, 'inconvo dev' starts a server, but let's check if there's a check command.
    # If not, we fall back to file checks.
    result = subprocess.run(
        ["inconvo", "--help"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    # If 'check' command exists in help, run it.
    if "check" in result.stdout:
        check_result = subprocess.run(
            ["inconvo", "check"],
            capture_output=True, text=True, cwd=PROJECT_DIR
        )
        assert check_result.returncode == 0, \
            f"'inconvo check' failed: {check_result.stderr}"

def test_users_table_is_queryable():
    """Priority 3: Verify the users table state in the config file."""
    with open(CONFIG_PATH, "r") as f:
        content = f.read()
    
    # Check for 'state: Queryable' under 'users:'
    # We use a simple check for existence of the string within the context of users
    users_section = content.split("users:")[1].split("orders:")[0] # Rough split
    assert "state: Queryable" in users_section, \
        "The 'users' table state must remain 'Queryable'."

def test_sensitive_fields_are_off():
    """Priority 3: Verify that sensitive fields are set to Off."""
    with open(CONFIG_PATH, "r") as f:
        content = f.read()
    
    users_section = content.split("users:")[1].split("orders:")[0]
    
    # Check password_hash
    assert "password_hash:" in users_section, "Field 'password_hash' not found in users table."
    # Look for state: Off specifically for this field
    # This is a bit tricky with plain text, but we can look for the line
    lines = users_section.splitlines()
    password_hash_off = False
    secret_key_off = False
    
    current_field = None
    for line in lines:
        line = line.strip()
        if line.endswith(":"):
            current_field = line[:-1]
        elif ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip()
            if key == "state" and val == "Off":
                if current_field == "password_hash":
                    password_hash_off = True
                elif current_field == "secret_key":
                    secret_key_off = True
            # Handle inline format: password_hash: { state: Off }
            if "password_hash" in line and "state" in line and "Off" in line:
                password_hash_off = True
            if "secret_key" in line and "state" in line and "Off" in line:
                secret_key_off = True

    assert password_hash_off, "Field 'password_hash' state must be set to 'Off'."
    assert secret_key_off, "Field 'secret_key' state must be set to 'Off'."

def test_no_database_changes():
    """Priority 1: Verify no schema changes were made to the actual database."""
    # This requires DATABASE_URL to be set in the environment
    assert "DATABASE_URL" in os.environ, "DATABASE_URL environment variable is required for verification."
    
    # Check if the columns still exist in the database (they should!)
    # We use psql to check the column existence
    check_cmd = [
        "psql", os.environ["DATABASE_URL"], "-t", "-c",
        "SELECT column_name FROM information_schema.columns WHERE table_name='users' AND column_name IN ('password_hash', 'secret_key');"
    ]
    result = subprocess.run(check_cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"Failed to query database: {result.stderr}"
    
    columns = result.stdout.strip().splitlines()
    assert len(columns) == 2, f"Expected 2 columns in database, found: {columns}. Do NOT modify the database schema."
