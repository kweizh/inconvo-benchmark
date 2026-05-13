import os
import shutil
import pytest

def test_node_installed():
    assert shutil.which("node") is not None, "node binary not found in PATH."
    assert shutil.which("npm") is not None, "npm binary not found in PATH."

def test_env_vars_present():
    assert "INCONVO_API_KEY" in os.environ, "INCONVO_API_KEY is missing."
    assert "INCONVO_AGENT_ID" in os.environ, "INCONVO_AGENT_ID is missing."
