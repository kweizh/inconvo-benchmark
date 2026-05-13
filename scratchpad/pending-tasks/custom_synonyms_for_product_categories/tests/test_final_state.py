import os
import subprocess
import json
import pytest

def test_model_pull_and_synonyms():
    # Ensure environment variables are set
    agent_id = os.environ.get("INCONVO_AGENT_ID")
    api_key = os.environ.get("INCONVO_API_KEY")
    assert agent_id is not None, "INCONVO_AGENT_ID environment variable is not set."
    assert api_key is not None, "INCONVO_API_KEY environment variable is not set."

    # Pull the model using the CLI
    result = subprocess.run(
        ["npx", "inconvo", "model", "pull", "--agent", agent_id, "--api-key", api_key],
        capture_output=True, text=True, cwd="/home/user/project"
    )
    assert result.returncode == 0, f"'inconvo model pull' failed: {result.stderr}"

    # Verify the model contains the synonyms
    # The model is pulled into .inconvo/ directory. We can find the products table file.
    model_dir = "/home/user/project/.inconvo"
    assert os.path.isdir(model_dir), f"Expected model directory {model_dir} to exist."

    # Look for products table in the YAML files
    found_products = False
    found_synonyms = False
    
    for root, _, files in os.walk(model_dir):
        for file in files:
            if file.endswith(".yaml") or file.endswith(".yml"):
                file_path = os.path.join(root, file)
                with open(file_path, "r") as f:
                    content = f.read()
                    
                    if "products:" in content or "name: products" in content:
                        found_products = True
                        if "product_category:" in content:
                            if "type" in content and "kind" in content and "class" in content and "synonyms" in content:
                                found_synonyms = True

    assert found_products, "Could not find 'products' table in the pulled semantic model."
    assert found_synonyms, "Could not find 'type', 'kind', and 'class' synonyms for 'product_category' in the 'products' table."
