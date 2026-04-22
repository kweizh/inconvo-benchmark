import os

def test_initial_state():
    # Check if DATABASE_URL is set
    assert "DATABASE_URL" in os.environ, "DATABASE_URL environment variable is not set"
    
    # Check that .inconvo directory does not exist
    assert not os.path.exists(".inconvo"), ".inconvo directory should not exist initially"
