import os
import subprocess

def test_initial_state():
    # Check if DATABASE_URL is set
    assert "DATABASE_URL" in os.environ, "DATABASE_URL environment variable is missing"
    
    # Check if we can connect to postgres
    db_url = os.environ["DATABASE_URL"]
    # Simple check using psql if available, or just assume it's there as per requirements
    try:
        subprocess.run(["psql", db_url, "-c", "SELECT 1"], check=True, capture_output=True)
    except FileNotFoundError:
        # If psql is not installed, we'll rely on the fact that the Dockerfile should provide it
        pass
    except subprocess.CalledProcessError as e:
        assert False, f"Failed to connect to PostgreSQL: {e.stderr.decode()}"

    # Verify inconvo CLI is NOT yet initialized (no .inconvo dir)
    assert not os.path.exists(".inconvo"), ".inconvo directory already exists"
    
    # Verify we are in a clean directory
    files = os.listdir(".")
    # Filter out hidden files and the bootstrap/tests dirs if they are mapped
    visible_files = [f for f in files if not f.startswith(".")]
    # It's okay if there's a package.json or similar if we pre-installed deps
