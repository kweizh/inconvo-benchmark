import os
import subprocess
import time
import socket
import urllib.request
import urllib.error
import json
import pytest

PROJECT_DIR = "/home/user/inconvo-express"

def wait_for_port(port, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', port)) == 0:
                return True
        time.sleep(0.5)
    return False

@pytest.fixture(scope="module")
def start_app():
    # Create mock.js to intercept fetch calls from the Inconvo SDK
    mock_js_path = os.path.join(PROJECT_DIR, "mock.js")
    with open(mock_js_path, "w") as f:
        f.write("""
const originalFetch = global.fetch;
global.fetch = async (...args) => {
    const url = args[0].toString();
    // Intercept inconvo API calls
    if (url.includes('inconvo')) {
        return new Response(JSON.stringify({ id: "conv_mock_123", message: "Mocked response" }), {
            status: 200,
            headers: { 'Content-Type': 'application/json' }
        });
    }
    return originalFetch(...args);
};
""")
    
    env = os.environ.copy()
    env["INCONVO_API_KEY"] = "test_api_key_123"
    env["INCONVO_AGENT_ID"] = "agent_456"
    env["NODE_OPTIONS"] = "--require ./mock.js"

    process = subprocess.Popen(
        ["node", "index.js"],
        cwd=PROJECT_DIR,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )

    if not wait_for_port(3000):
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        stderr_output = process.stderr.read().decode()
        pytest.fail(f"Express app failed to start and listen on port 3000. stderr: {stderr_output}")

    yield

    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=5)

def test_express_endpoint_responds(start_app):
    req = urllib.request.Request(
        "http://localhost:3000/ask",
        data=json.dumps({"question": "What is my revenue?", "userId": "user_123"}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            assert response.status == 200, f"Expected 200 OK, got {response.status}"
            body = response.read().decode("utf-8")
            assert body, "Response body should not be empty"
            
            try:
                data = json.loads(body)
                assert isinstance(data, dict), "Response should be a JSON object"
            except json.JSONDecodeError:
                pass # As long as it returns something, it's fine, the exact format wasn't strictly constrained
                
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        pytest.fail(f"HTTP Error {e.code} from Express server: {error_body}")
    except Exception as e:
        pytest.fail(f"Request to Express server failed: {str(e)}")

def test_index_js_exists():
    assert os.path.isfile(os.path.join(PROJECT_DIR, "index.js")), "index.js not found in project directory"

def test_package_json_dependencies():
    pkg_path = os.path.join(PROJECT_DIR, "package.json")
    assert os.path.isfile(pkg_path), "package.json not found"
    with open(pkg_path, "r") as f:
        pkg = json.load(f)
    deps = pkg.get("dependencies", {})
    assert "express" in deps, "express not found in dependencies"
    assert "@inconvoai/node" in deps, "@inconvoai/node not found in dependencies"
