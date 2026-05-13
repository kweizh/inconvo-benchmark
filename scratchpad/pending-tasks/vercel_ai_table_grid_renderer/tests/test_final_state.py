import os
import signal
import socket
import subprocess
import time

import pytest
from pochi_verifier import PochiVerifier

PROJECT_DIR = "/home/user/app"


def wait_for_port(port: int, timeout: int = 120) -> bool:
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(("localhost", port)) == 0:
                return True
        time.sleep(2)
    return False


@pytest.fixture(scope="module")
def start_app():
    # Ensure a clean production build for the implemented component.
    build = subprocess.run(
        ["npm", "run", "build"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
    )
    assert build.returncode == 0, (
        f"'npm run build' failed:\nSTDOUT:\n{build.stdout}\nSTDERR:\n{build.stderr}"
    )

    process = subprocess.Popen(
        ["npm", "start"],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid,
    )

    if not wait_for_port(3000, timeout=120):
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("Next.js app failed to start and listen on port 3000.")

    yield

    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    try:
        process.wait(timeout=30)
    except subprocess.TimeoutExpired:
        os.killpg(os.getpgid(process.pid), signal.SIGKILL)


def test_table_grid_renders_and_is_sortable(start_app):
    reason = (
        "The Next.js app must render Inconvo table tool outputs using a sortable "
        "data grid component (InconvoTableGrid) that exposes "
        "data-testid=\"inconvo-table-grid\" and supports column-header click to toggle sort."
    )
    truth = (
        "Navigate to http://localhost:3000. Verify that a chat input field is visible "
        "near the bottom of the page. Click the input field, type 'Show me the top 5 products', "
        "and press Enter. Wait for the assistant to respond (up to 60 seconds). "
        "Verify that an HTML <table> element with attribute data-testid=\"inconvo-table-grid\" "
        "appears in the conversation. Verify that the table contains a <thead> with one or more "
        "<th> column headers and a <tbody> with one or more <tr> rows of <td> cells. "
        "Click the first column header (the first <th>) once and verify that the row order "
        "in <tbody> changes (ascending sort) and the aria-sort attribute of that header "
        "becomes 'ascending' (or a visible ascending-arrow indicator such as '▲' appears next "
        "to the header label). Click the same header a second time and verify that the row "
        "order changes again (descending sort) and the aria-sort attribute becomes 'descending' "
        "(or a descending-arrow indicator such as '▼' appears)."
    )

    verifier = PochiVerifier()
    result = verifier.verify(
        reason=reason,
        truth=truth,
        use_browser_agent=True,
        trajectory_dir="/logs/verifier/pochi/test_table_grid",
    )
    assert result.status == "pass", f"Browser verification failed: {result.reason}"
