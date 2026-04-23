import os
import yaml
import sys

def test_final_state():
    project_dir = "/home/user/myproject"
    yaml_path = os.path.join(project_dir, "inconvo.yaml")
    
    if not os.path.exists(yaml_path):
        print(f"File {yaml_path} does not exist.")
        sys.exit(1)
        
    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f)
        
    # Check tables
    orders = data.get("tables", {}).get("orders", {})
    if orders.get("state") != "Queryable":
        print("orders table state is not Queryable.")
        sys.exit(1)
        
    customers = data.get("tables", {}).get("customers", {})
    if customers.get("state") != "Joinable":
        print("customers table state is not Joinable.")
        sys.exit(1)
        
    # Check fields
    total_amount = orders.get("fields", {}).get("total_amount", {})
    if total_amount.get("type") != "measure":
        print("orders.total_amount type is not measure.")
        sys.exit(1)
        
    created_at = orders.get("fields", {}).get("created_at", {})
    if created_at.get("type") != "dimension":
        print("orders.created_at type is not dimension.")
        sys.exit(1)
        
    # Check relations
    relations = data.get("relations", [])
    relation_found = False
    for rel in relations:
        if rel.get("name") == "order_to_customer":
            if rel.get("left") == "orders.customer_id" and rel.get("right") == "customers.id":
                relation_found = True
                break
                
    if not relation_found:
        print("relation order_to_customer with left: orders.customer_id and right: customers.id not found.")
        sys.exit(1)
        
    print("Final state is correct.")
    sys.exit(0)

if __name__ == "__main__":
    test_final_state()