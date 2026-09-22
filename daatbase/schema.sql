CREATE DATABASE IF NOT EXISTS ecommerce_intelligence;

USE ecommerce_intelligence;

-- 1. Customers
CREATE TABLE customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    customer_name VARCHAR(150) NOT NULL,
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100)
);

-- 2. Products
CREATE TABLE products (
    product_id VARCHAR(50) PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    brand VARCHAR(100)
);

-- 3. Sellers
CREATE TABLE sellers (
    seller_id VARCHAR(50) PRIMARY KEY
);

-- 4. Orders
CREATE TABLE orders (
    order_id VARCHAR(50) PRIMARY KEY,
    order_date DATE NOT NULL,
    customer_id VARCHAR(50),
    seller_id VARCHAR(50),
    payment_method VARCHAR(50),
    order_status VARCHAR(50),

    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id),

    FOREIGN KEY (seller_id)
        REFERENCES sellers(seller_id)
);

-- 5. Order Items
CREATE TABLE order_items (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id VARCHAR(50),
    product_id VARCHAR(50),
    quantity INT,
    unit_price DECIMAL(12,2),
    discount DECIMAL(12,2),
    tax DECIMAL(12,2),
    shipping_cost DECIMAL(12,2),
    total_amount DECIMAL(12,2),

    FOREIGN KEY (order_id)
        REFERENCES orders(order_id),

    FOREIGN KEY (product_id)
        REFERENCES products(product_id)
);