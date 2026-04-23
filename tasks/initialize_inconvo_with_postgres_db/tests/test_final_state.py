import os
import yaml
import subprocess

PROJECT_DIR = "/home/user/myproject"

def test_env_file_contains_database_url():
    env_path = os.path.join(PROJECT_DIR, ".env")
    assert os.path.isfile(env_path), f".env file {env_path} does not exist."
    
    with open(env_path, 'r') as f:
        content = f.read()
        
    assert "DATABASE_URL=postgresql://inconvo:inconvo@localhost:5432/inconvo_db" in content, \
        f"Expected DATABASE_URL to be set in .env, got: {content}"

def test_inconvo_yaml_exists():
    config_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    assert os.path.isfile(config_path), f"Config file {config_path} does not exist."
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
        
    assert config is not None, "inconvo.yaml is empty or invalid"
    assert 'tables' in config or 'connections' in config or 'models' in config, "inconvo.yaml does not look like a valid semantic model"

def test_database_connection():
    result = subprocess.run(
        ["psql", "postgresql://inconvo:inconvo@localhost:5432/inconvo_db", "-c", "\\conninfo"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Failed to connect to the database: {result.stderr}"
