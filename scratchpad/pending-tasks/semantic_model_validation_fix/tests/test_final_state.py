import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/inconvo-project"

def test_model_push_succeeds():
    """Priority 1: Use Inconvo CLI to verify the model is valid and can be pushed."""
    # Ensure the environment has the necessary variables
    env = os.environ.copy()
    if "INCONVO_POSTGRESQL_URL" in env:
        env["DATABASE_URL"] = env["INCONVO_POSTGRESQL_URL"]

    result = subprocess.run(
        ["npx", "inconvo", "model", "push"],
        capture_output=True, text=True, cwd=PROJECT_DIR, env=env
    )
    assert result.returncode == 0, \
        f"'npx inconvo model push' failed. The semantic model might still be invalid or ambiguous.\nStdout: {result.stdout}\nStderr: {result.stderr}"

def test_inconvo_yaml_syntax_fixed():
    """Priority 3 fallback: check that inconvo.yaml exists and is valid YAML."""
    import yaml
    yaml_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    
    try:
        with open(yaml_path, 'r') as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        pytest.fail(f"inconvo.yaml contains syntax errors: {e}")
        
    assert "relations" in data, "inconvo.yaml is missing the 'relations' section."
