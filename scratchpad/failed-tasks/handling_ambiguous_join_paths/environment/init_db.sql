CREATE TABLE addresses (
    id SERIAL PRIMARY KEY,
    street TEXT,
    city TEXT,
    state TEXT,
    zip TEXT
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    total_amount DECIMAL,
    shipping_address_id INTEGER REFERENCES addresses(id),
    billing_address_id INTEGER REFERENCES addresses(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert some dummy data
INSERT INTO addresses (street, city, state, zip) VALUES ('123 Shipping St', 'ShipCity', 'SC', '12345');
INSERT INTO addresses (street, city, state, zip) VALUES ('456 Billing Ave', 'BillTown', 'BT', '67890');
INSERT INTO orders (total_amount, shipping_address_id, billing_address_id) VALUES (100.00, 1, 2);
