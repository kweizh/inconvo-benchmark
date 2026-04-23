import os
import shutil
import subprocess
import pytest
import yaml

PROJECT_DIR = "/home/user/myproject"

def test_working_directory_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_initial_semantic_model_exists():
    model_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    assert os.path.isfile(model_path), f"Semantic model file {model_path} does not exist."

def test_initial_semantic_model_content():
    model_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    with open(model_path) as f:
        data = yaml.safe_load(f)
    assert "tables" in data, "Expected initial inconvo.yaml to have a tables key."
