import os
import yaml

def test_initial_state():
    assert os.path.exists('/home/user/myproject/inconvo.yaml')
    with open('/home/user/myproject/inconvo.yaml', 'r') as f:
        config = yaml.safe_load(f)
    assert 'users' in config.get('tables', {})
    assert 'is_active' not in config['tables']['users'].get('fields', {})
