import os
import pytest

PROJECT_DIR = "/home/user/myproject"

def test_relationship_defined():
    """Priority 3 fallback: basic file check for relationship."""
    config_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    with open(config_path) as f:
        content = f.read()
    
    assert "relations:" in content, "Expected 'relations' list in inconvo.yaml."
    assert "user_to_profile" in content, "Expected 'user_to_profile' relationship name in inconvo.yaml."
    assert "users.profile_id" in content, "Expected 'users.profile_id' in relationship left/right fields."
    assert "profiles.id" in content, "Expected 'profiles.id' in relationship left/right fields."