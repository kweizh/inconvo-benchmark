# Financial Schema Mapping with Inconvo

## Background
You are building a chat-with-data agent for a financial application using Inconvo. You need to map a database schema consisting of `transactions`, `accounts`, and `customers` into a semantic model.

## Requirements
- Initialize an Inconvo project in `/home/user/financial-agent`.
- Configure the `inconvo.yaml` semantic model with the following:
  - `transactions` table: state `Queryable`.
    - Fields: `amount` (state: On, type: measure), `transaction_date` (state: On, type: dimension), `net_flow` (state: On, type: measure, sql: `sum(case when type = 'credit' then amount else -amount end)`).
  - `accounts` table: state `Joinable`.
    - Add a context filter to restrict access to `tenant_id = {{context.tenant_id}}`.
  - `customers` table: state `Joinable`.
  - Relations:
    - `transaction_to_account`: left `transactions.account_id`, right `accounts.id`.
    - `account_to_customer`: left `accounts.customer_id`, right `customers.id`.

## Implementation Guide
1. Create the directory `/home/user/financial-agent`.
2. Create or generate the `inconvo.yaml` file in `/home/user/financial-agent`.
3. Populate the `inconvo.yaml` file with the required tables, fields, and relations as specified above.

## Constraints
- Project path: `/home/user/financial-agent`

## Integrations
- None