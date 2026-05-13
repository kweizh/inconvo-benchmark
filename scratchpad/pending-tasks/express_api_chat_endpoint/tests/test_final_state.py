import json
import os
import signal
import socket
import subprocess
import time
import urllib.error
import urllib.request

import pytest

PROJECT_DIR = "/home/user/inconvo-app"
INDEX_JS = os.path.join(PROJECT_DIR, "index.js")
PORT = 3001
BASE_URL = f"http://localhost:{PORT}"


def wait_for_port(port, timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(("localhost", port)) == 0:
                return True
        time.sleep(1)
    return False


@pytest.fixture(scope="module")
def start_server():
    assert os.path.isfile(INDEX_JS), f"index.js not found at {INDEX_JS}"

    env = os.environ.copy()
    # Required env vars must be provided by the verifier environment.
    for key in ("INCONVO_API_KEY", "INCONVO_AGENT_ID", "INCONVO_DB_URL"):
        if key not in env or not env[key]:
            pytest.fail(
                f"Required env var '{key}' is not set in the verifier environment."
            )

    process = subprocess.Popen(
        ["node", "index.js"],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        preexec_fn=os.setsid,
    )

    if not wait_for_port(PORT, timeout=60):
        try:
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        except ProcessLookupError:
            pass
        stdout, stderr = process.communicate(timeout=10)
        pytest.fail(
            "Express server did not start listening on port "
            f"{PORT} within 60 seconds.\nstdout:\n{stdout.decode('utf-8', 'replace')}\n"
            f"stderr:\n{stderr.decode('utf-8', 'replace')}"
        )

    yield process

    try:
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    except ProcessLookupError:
        pass
    try:
        process.wait(timeout=15)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(os.getpgid(process.pid), signal.SIGKILL)
        except ProcessLookupError:
            pass


def _http_post(path, payload):
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        BASE_URL + path,
        data=body,
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return resp.getcode(), resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")


def test_index_js_exists():
    assert os.path.isfile(INDEX_JS), f"index.js not found at {INDEX_JS}"


def test_index_js_content_references_required_apis():
    with open(INDEX_JS, "r") as f:
        content = f.read()

    assert "express" in content, "Expected 'express' to be imported/required in index.js"
    assert "@inconvoai/node" in content, (
        "Expected '@inconvoai/node' to be imported/required in index.js"
    )
    assert "INCONVO_API_KEY" in content, (
        "Expected the server to read INCONVO_API_KEY from the environment in index.js"
    )
    assert "INCONVO_AGENT_ID" in content, (
        "Expected the server to read INCONVO_AGENT_ID from the environment in index.js"
    )
    assert "3001" in content, "Expected the server to listen on port 3001 in index.js"
    assert "/chat" in content, "Expected a /chat route to be defined in index.js"


def test_missing_message_returns_400(start_server):
    status, body = _http_post("/chat", {"userId": "user-123"})
    assert status == 400, (
        f"Expected HTTP 400 when 'message' is missing, got {status}. Body: {body}"
    )
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        pytest.fail(f"Expected JSON error body for 400 response, got: {body}")
    # The body should describe the missing message field in some form.
    body_lower = json.dumps(data).lower()
    assert "message" in body_lower, (
        f"Expected error body to reference the missing 'message' field, got: {data}"
    )


def test_valid_request_returns_inconvo_response(start_server):
    status, body = _http_post(
        "/chat",
        {"message": "What are my top products?", "userId": "user-123"},
    )
    assert status == 200, (
        f"Expected HTTP 200 for a valid /chat request, got {status}. Body: {body}"
    )

    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        pytest.fail(f"Response body from /chat is not valid JSON: {body}")

    # Ensure the response is not a thin error envelope produced by the route itself.
    if isinstance(data, dict):
        assert data.get("error") in (None, False), (
            f"Response indicates an error from the Express handler: {data}"
        )

    serialized = json.dumps(data).lower()
    # A real Inconvo response should carry one of these structural keys.
    expected_markers = ("type", "text", "table", "data", "rows", "message", "content", "id")
    assert any(marker in serialized for marker in expected_markers), (
        "Response does not look like a real Inconvo agent response. "
        f"Content: {data}"
    )
