import os
import re
import subprocess
import pytest

PROJECT_DIR = "/home/user/inconvo-app"
YAML_PATH = os.path.join(PROJECT_DIR, "inconvo.yaml")

def test_internal_id_is_off():
    with open(YAML_PATH, "r") as f:
        content = f.read()
    
    match = re.search(r'internal_id:\s*\{[^}]*state:\s*Off[^}]*\}', content)
    if not match:
        match = re.search(r'internal_id:\s*\n(?:\s+.*\n)*\s+state:\s*Off', content)
        if not match:
            # Maybe with quotes
            match = re.search(r'internal_id:[\s\S]*?state:\s*[\'"]Off[\'"]', content)
        
    assert match is not None, "Expected 'internal_id' to have state: Off in inconvo.yaml"

def test_title_has_synonyms():
    with open(YAML_PATH, "r") as f:
        content = f.read()
        
    assert "name" in content and "item name" in content, "Synonyms 'name' and 'item name' not found in inconvo.yaml"
    
    match = re.search(r'title:\s*\{[^}]*synonyms:\s*\[[^\]]*\][^}]*\}', content)
    if not match:
        match = re.search(r'title:[\s\S]*?synonyms:[\s\S]*?(?:name|item name)', content)
        
    assert match is not None, "Expected 'title' to have synonyms ['name', 'item name'] in inconvo.yaml"

def test_total_amount_has_synonyms():
    with open(YAML_PATH, "r") as f:
        content = f.read()
        
    assert "revenue" in content, "Synonym 'revenue' not found in inconvo.yaml"
    
    match = re.search(r'total_amount:\s*\{[^}]*synonyms:\s*\[[^\]]*\][^}]*\}', content)
    if not match:
        match = re.search(r'total_amount:[\s\S]*?synonyms:[\s\S]*?revenue', content)
        
    assert match is not None, "Expected 'total_amount' to have synonyms ['revenue'] in inconvo.yaml"

def test_run_index_js():
    # Run the script that interacts with the SDK or validates the setup
    result = subprocess.run(
        ["node", "index.js"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"'node index.js' failed with output: {result.stderr}\n{result.stdout}"
