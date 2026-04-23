import os
import subprocess
import time
import socket
import pytest
from pochi_verifier import PochiVerifier

PROJECT_DIR = "/home/user/app"

def wait_for_port(port, timeout=120):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', port)) == 0:
                return True
        time.sleep(5)
    return False

@pytest.fixture(scope="module")
def start_app():
    # Build the app first
    build_process = subprocess.run(
        ["npm", "run", "build"],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if build_process.returncode != 0:
        pytest.fail(f"Build failed: {build_process.stderr.decode('utf-8')}")
    
    # Start the app
    process = subprocess.Popen(
        ["npm", "start"],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )
    
    # Wait for the app to be ready
    if not wait_for_port(3000):
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("App failed to start and listen on required ports.")
    
    yield
    
    # Shut down the app
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=30)

def test_api_route_configured_correctly():
    """Priority 3 fallback: Verify API route implementation."""
    api_route_path = os.path.join(PROJECT_DIR, "app/api/chat/route.ts")
    assert os.path.isfile(api_route_path), f"API route not found at {api_route_path}"
    
    with open(api_route_path, "r") as f:
        content = f.read()
        
    assert "inconvoDataAgent" in content, "Expected 'inconvoDataAgent' to be used in API route."
    assert "user-123" in content, "Expected 'userIdentifier: \"user-123\"' in API route."
    assert "organisationId" in content and "1" in content, "Expected 'organisationId: 1' in API route context."

def test_page_uses_use_chat():
    """Priority 3 fallback: Verify page uses useChat."""
    page_path = os.path.join(PROJECT_DIR, "app/page.tsx")
    assert os.path.isfile(page_path), f"Page not found at {page_path}"
    
    with open(page_path, "r") as f:
        content = f.read()
        
    assert "useChat" in content, "Expected 'useChat' hook to be used in page.tsx."

def test_browser_ui(start_app):
    """Priority 2: Use pochi-verifier to verify the UI."""
    reason = "The application should have a chat interface for asking about data."
    truth = "Navigate to http://localhost:3000. Verify that an input field with the placeholder \"Ask about your data...\" is visible."

    verifier = PochiVerifier()
    result = verifier.verify(
        reason=reason,
        truth=truth,
        use_browser_agent=True,
        trajectory_dir="/logs/verifier/pochi/test_browser_ui"
    )
    assert result.status == "pass", f"Browser verification failed: {result.reason}"
