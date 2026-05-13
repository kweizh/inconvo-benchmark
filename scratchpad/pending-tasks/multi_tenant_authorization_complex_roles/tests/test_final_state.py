import os
import subprocess
import json
import pytest

PROJECT_DIR = "/home/user/inconvo-app"

def test_inconvo_yaml_exists_and_contains_orders():
    yaml_path = os.path.join(PROJECT_DIR, "inconvo.yaml")
    assert os.path.isfile(yaml_path), f"inconvo.yaml not found at {yaml_path}"

    with open(yaml_path, "r") as f:
        content = f.read()

    assert "orders" in content, "Expected 'orders' table definition in inconvo.yaml"
    assert "store_id" in content, "Expected 'store_id' field definition in inconvo.yaml"

def test_index_js_logic():
    index_path = os.path.join(PROJECT_DIR, "index.js")
    assert os.path.isfile(index_path), f"index.js not found at {index_path}"

    # Create a test script to mock the SDK and test the askQuestion function
    test_script_path = os.path.join(PROJECT_DIR, "test_run.js")
    test_script_content = """
const fs = require('fs');
const path = require('path');

// Mock @inconvoai/node
const mockInconvo = {
    Inconvo: class {
        constructor(config) {
            this.config = config;
            this.conversations = {
                create: async (params) => {
                    return { id: 'conv_123', context: params.context };
                },
                messages: {
                    create: async (id, params) => {
                        return { text: 'mock response' };
                    }
                }
            };
        }
    }
};

// Override require to serve the mock for @inconvoai/node
const Module = require('module');
const originalRequire = Module.prototype.require;
Module.prototype.require = function(request) {
    if (request === '@inconvoai/node') {
        return mockInconvo;
    }
    return originalRequire.apply(this, arguments);
};

async function runTests() {
    try {
        const { askQuestion } = require('./index.js');
        if (typeof askQuestion !== 'function') {
            console.error(JSON.stringify({ error: 'askQuestion is not a function' }));
            process.exit(1);
        }

        // Test store_manager
        // To test the context passed to conversations.create, we need a way to spy on it.
        // Let's modify the mock to capture the context.
        let capturedContext = null;
        mockInconvo.Inconvo = class {
            constructor() {
                this.conversations = {
                    create: async (params) => {
                        capturedContext = params.context;
                        return { id: 'conv_123' };
                    },
                    messages: {
                        create: async () => ({ text: 'ok' })
                    }
                };
            }
        };

        await askQuestion('sales?', { role: 'store_manager', store_id: 42 });
        const storeManagerContext = capturedContext;

        capturedContext = null;
        await askQuestion('sales?', { role: 'admin' });
        const adminContext = capturedContext;

        console.log(JSON.stringify({
            storeManagerContext,
            adminContext
        }));
    } catch (e) {
        console.error(JSON.stringify({ error: e.message }));
        process.exit(1);
    }
}

runTests();
"""
    with open(test_script_path, "w") as f:
        f.write(test_script_content)

    result = subprocess.run(
        ["node", "test_run.js"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Test script failed: {result.stderr}\n{result.stdout}"

    try:
        output = json.loads(result.stdout)
    except json.JSONDecodeError:
        pytest.fail(f"Failed to parse test script output: {result.stdout}")

    assert "error" not in output, f"Error in index.js: {output.get('error')}"
    
    # Store manager should have store_id in context
    sm_context = output.get("storeManagerContext") or {}
    assert "store_id" in sm_context, f"Store manager context missing store_id: {sm_context}"
    assert sm_context["store_id"] == 42, f"Store manager context has wrong store_id: {sm_context}"

    # Admin should not have store_id filter, or it should be empty/allow-all
    # Depending on implementation, they might pass no context or empty context
    admin_context = output.get("adminContext")
    if admin_context is not None:
        assert "store_id" not in admin_context, f"Admin context should not filter by store_id: {admin_context}"
