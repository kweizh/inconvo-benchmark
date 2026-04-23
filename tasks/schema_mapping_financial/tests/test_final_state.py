import os
import pytest

PROJECT_DIR = "/home/user/financial-agent"
MODEL_FILE = os.path.join(PROJECT_DIR, "inconvo.yaml")

def test_project_directory_exists():
    assert os.path.isdir(PROJECT_DIR), f"Project directory {PROJECT_DIR} does not exist."

def test_model_file_exists():
    assert os.path.isfile(MODEL_FILE), f"Semantic model file {MODEL_FILE} does not exist."

def test_transactions_table_configured():
    with open(MODEL_FILE, "r") as f:
        content = f.read()
    
    # Check transactions table state
    assert "transactions:" in content, "Expected 'transactions' table in inconvo.yaml."
    assert "Queryable" in content, "Expected 'transactions' state to be 'Queryable'."
    
    # Check fields
    assert "amount:" in content, "Expected 'amount' field in 'transactions'."
    assert "measure" in content, "Expected 'amount' to be a 'measure'."
    assert "transaction_date:" in content, "Expected 'transaction_date' field in 'transactions'."
    assert "dimension" in content, "Expected 'transaction_date' to be a 'dimension'."
    
    # Check net_flow
    assert "net_flow:" in content, "Expected 'net_flow' field in 'transactions'."
    assert "sum(case when type = 'credit' then amount else -amount end)" in content or "sum(case when type = 'credit' then amount else -amount end)" in content.replace('"', "'"), "Expected correct SQL definition for 'net_flow'."

def test_accounts_and_customers_configured():
    with open(MODEL_FILE, "r") as f:
        content = f.read()
    
    # Check accounts table state
    assert "accounts:" in content, "Expected 'accounts' table in inconvo.yaml."
    assert "Joinable" in content, "Expected 'accounts' and 'customers' state to be 'Joinable'."
    
    # Check context filter
    assert "tenant_id = {{context.tenant_id}}" in content or "tenant_id = {{ context.tenant_id }}" in content, "Expected context filter for tenant_id on 'accounts' table."
    
    # Check customers table
    assert "customers:" in content, "Expected 'customers' table in inconvo.yaml."

def test_relations_configured():
    with open(MODEL_FILE, "r") as f:
        content = f.read()
    
    # Check relations
    assert "relations:" in content, "Expected 'relations' section in inconvo.yaml."
    assert "transaction_to_account" in content, "Expected 'transaction_to_account' relation."
    assert "transactions.account_id" in content, "Expected 'transactions.account_id' in relation 'transaction_to_account'."
    assert "accounts.id" in content, "Expected 'accounts.id' in relation 'transaction_to_account'."
    
    assert "account_to_customer" in content, "Expected 'account_to_customer' relation."
    assert "accounts.customer_id" in content, "Expected 'accounts.customer_id' in relation 'account_to_customer'."
    assert "customers.id" in content, "Expected 'customers.id' in relation 'account_to_customer'."
