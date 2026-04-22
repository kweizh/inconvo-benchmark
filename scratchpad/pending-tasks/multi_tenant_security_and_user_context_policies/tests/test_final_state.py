import os
import subprocess
import json
import time
import socket
import pytest
from pochi_verifier import PochiVerifier

PROJECT_DIR = "/home/user/analytics-platform"

def wait_for_port(port, timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', port)) == 0:
                return True
        time.sleep(5)
    return False

@pytest.fixture(scope="module")
def start_inconvo():
    # Start the inconvo dev server
    # We assume DATABASE_URL is already in the environment
    process = subprocess.Popen(
        ["inconvo", "dev"],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )
    
    # Wait for the server to be ready (default port for inconvo dev is usually 8000 or similar, 
    # but the API is what we test. Let's assume it listens on 8000 for the preview/API)
    # The documentation mentions 'inconvo dev' starts a local server.
    if not wait_for_port(8000, timeout=60):
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        # We don't fail here if port 8000 isn't the right one, 
        # but inconvo dev should start something.
        # If it fails, the verifier will fail anyway.
    
    yield process
    
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=10)

def test_semantic_model_config():
    """Priority 3: Verify the configuration file exists and has the correct policy."""
    config_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    assert os.path.isfile(config_path), f"inconvo.yaml not found at {config_path}"
    
    with open(config_path, 'r') as f:
        content = f.read()
    
    # Check for organisation_id mapping to context
    assert "organisation_id" in content, "organisation_id column not found in inconvo.yaml"
    assert "context.organisation_id" in content or "organisation_id: organisation_id" in content, \
        "Context filter for organisation_id not found or incorrectly configured in inconvo.yaml"

def test_multi_tenant_isolation(start_inconvo):
    """Priority 2: Use browser/agent verification to test data isolation."""
    reason = "The Inconvo agent must strictly enforce row-level security based on the organisation_id passed in the user context."
    truth = """
    1. Test Org 1: Create a conversation with context {"organisation_id": 1}. Ask "What is the total sales amount?". Verify the result only reflects data for organisation 1.
    2. Test Org 2: Create a conversation with context {"organisation_id": 2}. Ask "What is the total sales amount?". Verify the result only reflects data for organisation 2.
    3. Test Missing Context: Create a conversation without organisation_id in context. Ask for sales data and verify it returns no data or an error.
    """

    verifier = PochiVerifier()
    # Note: PochiVerifier can interact with the local server or use the CLI to simulate these calls if configured.
    # Since 'inconvo dev' provides a preview UI and API, the agent can use it.
    result = verifier.verify(
        reason=reason,
        truth=truth,
        use_browser_agent=True,
        trajectory_dir="/logs/verifier/pochi/test_multi_tenant_isolation"
    )
    assert result.status == "pass", f"Multi-tenant isolation verification failed: {result.reason}"
