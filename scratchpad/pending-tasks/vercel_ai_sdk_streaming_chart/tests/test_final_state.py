import os
import subprocess
import time
import socket
import json
import urllib.request
import urllib.error
import pytest

PROJECT_DIR = "/home/user/inconvo-ai-sdk-app"

def wait_for_port(port, timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', port)) == 0:
                return True
        time.sleep(5)
    return False

@pytest.fixture(scope="module")
def start_app():
    # Start the Next.js app
    process = subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )

    # Wait for the app to be ready
    if not wait_for_port(3000):
        # Kill the process group before failing
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("App failed to start and listen on port 3000.")

    yield

    # Shut down the app
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=30)

def test_project_structure():
    """Verify the project structure exists."""
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."
    assert os.path.isfile(os.path.join(PROJECT_DIR, "app/api/chat/route.ts")) or \
           os.path.isfile(os.path.join(PROJECT_DIR, "app/api/chat/route.js")), \
           "API route file (app/api/chat/route.ts or .js) not found."
    assert os.path.isfile(os.path.join(PROJECT_DIR, "app/page.tsx")) or \
           os.path.isfile(os.path.join(PROJECT_DIR, "app/page.js")), \
           "Page file (app/page.tsx or .js) not found."

def test_dependencies():
    """Verify the required packages are in package.json."""
    package_json_path = os.path.join(PROJECT_DIR, "package.json")
    assert os.path.isfile(package_json_path), "package.json not found."
    
    with open(package_json_path) as f:
        pkg = json.load(f)
    
    deps = pkg.get("dependencies", {})
    assert "ai" in deps, "The 'ai' package is missing from dependencies."
    assert "@ai-sdk/react" in deps, "The '@ai-sdk/react' package is missing from dependencies."
    assert "@inconvoai/vercel-ai-sdk" in deps, "The '@inconvoai/vercel-ai-sdk' package is missing from dependencies."

def test_chat_api_route(start_app):
    """Send a test POST request to the API route /api/chat and verify it returns a streaming response."""
    url = "http://localhost:3000/api/chat"
    data = json.dumps({
        "messages": [
            {"role": "user", "content": "Show me a chart of something."}
        ]
    }).encode('utf-8')
    
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')
    
    try:
        with urllib.request.urlopen(req) as response:
            assert response.status == 200, f"Expected status 200, got {response.status}"
            content = response.read().decode('utf-8')
            # The Vercel AI SDK stream should contain tool calls or stream parts.
            # Usually it starts with something like 0: or similar stream protocol.
            assert len(content) > 0, "Response body is empty."
            # We don't strictly assert the exact format because it can vary by Vercel AI SDK version,
            # but we verify it's a successful response and has content.
            # We can check if it looks like a stream (contains newlines or specific prefixes).
            assert "\n" in content or "{" in content, f"Response does not look like a stream or JSON: {content[:100]}"
    except urllib.error.HTTPError as e:
        error_content = e.read().decode('utf-8')
        pytest.fail(f"HTTP POST to /api/chat failed with status {e.code}: {error_content}")
    except Exception as e:
        pytest.fail(f"Failed to connect to /api/chat: {str(e)}")
