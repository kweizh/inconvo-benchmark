import os
import stat
import pytest

SCRIPT_FILE = "/home/user/project/run.sh"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_FILE), f"Script file {SCRIPT_FILE} does not exist."
    st = os.stat(SCRIPT_FILE)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {SCRIPT_FILE} is not executable."

def test_script_contains_required_command():
    with open(SCRIPT_FILE, 'r') as f:
        content = f.read()
    
    assert "npx inconvo" in content or "npx inconvo@latest" in content, "Expected 'npx inconvo' command in script."
    assert "model computed" in content, "Expected 'model computed' subcommand in script."
    assert "--agent agt_123" in content or "--agent=agt_123" in content, "Expected '--agent agt_123' in script."
    assert "--connection conn_456" in content or "--connection=conn_456" in content, "Expected '--connection conn_456' in script."
    assert "--dry-run" in content, "Expected '--dry-run' in script."
    
    # Check payload contents
    assert "orders" in content, "Expected table name 'orders' in payload."
    assert "gross_margin" in content, "Expected computed column name 'gross_margin' in payload."
    assert "revenue - cost" in content, "Expected expression 'revenue - cost' in payload."
