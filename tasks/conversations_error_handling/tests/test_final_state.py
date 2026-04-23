import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/inconvo-project"

def test_script_handles_error():
    # Setup mock @inconvoai/node
    mock_dir = os.path.join(PROJECT_DIR, "node_modules", "@inconvoai", "node")
    os.makedirs(mock_dir, exist_ok=True)
    
    package_json = os.path.join(mock_dir, "package.json")
    with open(package_json, "w") as f:
        f.write('{"name": "@inconvoai/node", "main": "index.js"}')
        
    index_js = os.path.join(mock_dir, "index.js")
    with open(index_js, "w") as f:
        f.write('''
class BadRequestError extends Error {
  constructor(message) {
    super(message);
    this.name = 'BadRequestError';
  }
}

class Inconvo {
  constructor(config) {}
  get agents() {
    return {
      conversations: {
        create: async (agentId, options) => {
          if (options && options.userContext && options.userContext.invalidKey) {
            throw new BadRequestError("400 Invalid userContext");
          }
          throw new Error("Unexpected error");
        }
      }
    };
  }
}

module.exports = Inconvo;
module.exports.default = Inconvo;
''')

    # Run the script
    env = os.environ.copy()
    env["INCONVO_API_KEY"] = "mock_key"
    env["INCONVO_AGENT_ID"] = "mock_agent"
    
    result = subprocess.run(
        ["node", "index.js"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
        env=env
    )
    
    assert result.returncode == 0, f"Script crashed or threw an error: {result.stderr}\\nStdout: {result.stdout}"
    
    # Check output.log
    log_file = os.path.join(PROJECT_DIR, "output.log")
    assert os.path.isfile(log_file), "output.log was not created."
    
    with open(log_file, "r") as f:
        content = f.read()
        
    assert "Context Error Handled" in content, f"Expected 'Context Error Handled' in output.log, got: {content}"
