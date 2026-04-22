import os
import subprocess
import time
import socket
import pytest
import json
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
    # Start the Next.js app in dev mode
    process = subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid,
        env=os.environ
    )
    
    # Wait for the app to be ready
    if not wait_for_port(3000):
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("Next.js app failed to start on port 3000.")
    
    yield process
    
    # Shut down the app
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=30)

def test_api_chat_endpoint():
    """Verify that the /api/chat endpoint exists and returns a stream."""
    import requests
    url = "http://localhost:3000/api/chat"
    payload = {
        "messages": [{"role": "user", "content": "Hello"}]
    }
    response = requests.post(url, json=payload, stream=True)
    assert response.status_code == 200, f"API endpoint failed with status {response.status_code}"
    assert "text/event-stream" in response.headers.get("Content-Type", ""), "Response is not a stream"

def test_streaming_ui_rendering(start_app):
    """Priority 2: Use Pochi Verifier to check the UI behavior."""
    reason = "The application should render a chat interface that handles Inconvo's streaming responses and displays data as UI components."
    truth = (
        "Navigate to http://localhost:3000. "
        "Type 'Show me total sales' in the input and submit. "
        "Verify that a loading state 'Querying your data...' is displayed. "
        "Wait for the response and verify that a table or chart component is rendered, "
        "not a raw JSON object or a markdown table."
    )

    verifier = PochiVerifier()
    result = verifier.verify(
        reason=reason,
        truth=truth,
        use_browser_agent=True,
        trajectory_dir="/logs/verifier/pochi/test_streaming_ui"
    )
    assert result.status == "pass", f"Browser verification failed: {result.reason}"

def test_file_structure():
    """Priority 3: Verify required files exist."""
    assert os.path.isfile(os.path.join(PROJECT_DIR, "app/api/chat/route.ts"))
    assert os.path.isfile(os.path.join(PROJECT_DIR, "app/page.tsx"))
    assert os.path.isdir(os.path.join(PROJECT_DIR, "app/components/inconvo"))
    
    # Check if dependencies are in package.json
    with open(os.path.join(PROJECT_DIR, "package.json")) as f:
        pkg = json.load(f)
        deps = pkg.get("dependencies", {})
        assert "@inconvoai/vercel-ai-sdk" in deps
        assert "ai" in deps
        assert "@ai-sdk/react" in deps
