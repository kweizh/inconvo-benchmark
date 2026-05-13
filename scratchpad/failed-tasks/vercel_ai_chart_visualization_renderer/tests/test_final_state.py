import os
import signal
import socket
import subprocess
import time

import pytest
from pochi_verifier import PochiVerifier

PROJECT_DIR = "/home/user/app"


def wait_for_port(port, timeout=120):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(("localhost", port)) == 0:
                return True
        time.sleep(5)
    return False


@pytest.fixture(scope="module")
def start_app():
    # Build the app first.
    build_process = subprocess.run(
        ["npm", "run", "build"],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if build_process.returncode != 0:
        pytest.fail(
            "npm run build failed:\nSTDOUT:\n"
            + build_process.stdout.decode("utf-8", errors="replace")
            + "\nSTDERR:\n"
            + build_process.stderr.decode("utf-8", errors="replace")
        )

    # Start the app.
    process = subprocess.Popen(
        ["npm", "start"],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid,
    )

    if not wait_for_port(3000):
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("Next.js app failed to start and listen on port 3000.")

    yield

    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=30)


def test_inconvo_chart_renders_in_browser(start_app):
    reason = (
        "The Next.js app must render Inconvo chart tool outputs as SVG bar charts. "
        "When the user asks for a chart, the response must include a DOM element "
        "with data-testid=\"inconvo-chart\" containing an <svg> chart visualization "
        "rendered by recharts."
    )
    truth = (
        "Navigate to http://localhost:3000. "
        "Verify that a chat input field is visible. "
        "Click the input, type exactly: Show me a bar chart of the top 5 products by total sales, "
        "then press Enter. "
        "Wait for the assistant's response to finish streaming (up to 90 seconds). "
        "Verify that the page now contains a DOM element matching the CSS selector "
        "[data-testid=\"inconvo-chart\"]. "
        "Verify that this element contains an <svg> element. "
        "Verify that the <svg> element contains at least 3 <rect> elements (one per bar) "
        "rendered by recharts."
    )

    verifier = PochiVerifier()
    result = verifier.verify(
        reason=reason,
        truth=truth,
        use_browser_agent=True,
        trajectory_dir="/logs/verifier/pochi/test_inconvo_chart",
    )
    assert result.status == "pass", (
        f"Browser verification failed: {result.reason}"
    )
