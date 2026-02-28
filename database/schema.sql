CREATE TABLE customers (
    customer_id TEXT PRIMARY KEY,
    gender TEXT,
    age INTEGER,
    city TEXT,
    signup_date DATE
);




CREATE TABLE transactions (
    transaction_id TEXT PRIMARY KEY,
    customer_id TEXT,
    product_id TEXT,
    quantity INTEGER,
    transaction_date DATE
);



CREATE TABLE customer_interactions (
    customer_id TEXT,
    category TEXT,
    interaction_date DATE
);
