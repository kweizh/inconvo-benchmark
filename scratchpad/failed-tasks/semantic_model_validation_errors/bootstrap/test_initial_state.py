import os
import yaml
import sys

def test_initial_state():
    project_dir = "/home/user/myproject"
    yaml_path = os.path.join(project_dir, "inconvo.yaml")
    
    if not os.path.exists(yaml_path):
        print(f"File {yaml_path} does not exist.")
        sys.exit(1)
        
    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f)
        
    # Check that it has errors initially
    orders_state = data.get("tables", {}).get("orders", {}).get("state")
    if orders_state == "Queryable":
        print("orders table state should not be Queryable initially.")
        sys.exit(1)
        
    customers_state = data.get("tables", {}).get("customers", {}).get("state")
    if customers_state == "Joinable":
        print("customers table state should not be Joinable initially.")
        sys.exit(1)
        
    print("Initial state is correct.")
    sys.exit(0)

if __name__ == "__main__":
    test_initial_state()