import os
import subprocess
import time
import json
import pytest
import socket

PROJECT_DIR = "/home/user/support-bot"

def wait_for_port(port, timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', port)) == 0:
                return True
        time.sleep(2)
    return False

@pytest.fixture(scope="module")
def run_inconvo_dev():
    # Start inconvo dev in the background
    # We use npx inconvo@latest dev
    process = subprocess.Popen(
        ["npx", "inconvo@latest", "dev"],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid,
        env=os.environ
    )
    
    # Wait for the server (default port is likely 8000 or similar, but let's check plan.md)
    # plan.md doesn't specify port, but typical dev servers use 8000 or 3000.
    # Actually, inconvo dev usually starts on 8000.
    if not wait_for_port(8000):
        # If 8000 doesn't work, maybe it's 3000?
        if not wait_for_port(3000):
             # Kill the process group before failing
            import signal
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
            pytest.fail("Inconvo dev server failed to start.")
    
    yield process
    
    # Shut down
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=10)

def test_inconvo_yaml_configuration():
    yaml_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    assert os.path.isfile(yaml_path), "inconvo.yaml not found."
    
    with open(yaml_path) as f:
        content = f.read()
    
    # Check tables
    assert "customers" in content, "Table 'customers' missing in inconvo.yaml"
    assert "orders" in content, "Table 'orders' missing in inconvo.yaml"
    assert "order_items" in content, "Table 'order_items' missing in inconvo.yaml"
    
    # Check states
    assert "state: Queryable" in content or "state: 'Queryable'" in content, "Tables should be set to Queryable"
    
    # Check relations
    assert "order_to_customer" in content, "Relation 'order_to_customer' missing"
    assert "item_to_order" in content, "Relation 'item_to_order' missing"

def test_query_latest_order_status(run_inconvo_dev):
    # Create a temporary test script
    test_script = os.path.join(PROJECT_DIR, "verify_query.js")
    with open(test_script, "w") as f:
        f.write("""
const { InconvoClient } = require('@inconvoai/node');
const client = new InconvoClient({ apiKey: 'local', baseUrl: 'http://localhost:8000' });

async function main() {
  try {
    const conversation = await client.conversations.create({});
    const response = await client.conversations.messages.create(conversation.id, {
      message: "What is the status of the latest order for customer 'Alice Smith'?"
    });
    console.log(JSON.stringify(response));
  } catch (e) {
    console.error(e);
    process.exit(1);
  }
}
main();
""")
    
    # Install SDK if needed
    subprocess.run(["npm", "install", "@inconvoai/node"], cwd=PROJECT_DIR, check=True)
    
    # Run the script
    result = subprocess.run(
        ["node", "verify_query.js"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0, f"Query script failed: {result.stderr}"
    
    # Check output for 'shipped'
    output = result.stdout.lower()
    assert "shipped" in output, f"Expected 'shipped' in query response, got: {output}"
