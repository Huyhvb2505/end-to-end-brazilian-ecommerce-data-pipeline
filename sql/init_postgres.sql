-- ==========================================
-- B. KHỞI TẠO DIMENSIONS (Có cột Audit)
-- ==========================================
CREATE TABLE dim_customer (
    customer_key BIGINT PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL,
    customer_unique_id VARCHAR(50) NOT NULL,
    customer_city VARCHAR(100),
    customer_state VARCHAR(2),
    inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE dim_product (
    product_key BIGINT PRIMARY KEY,
    product_id VARCHAR(50) NOT NULL,
    category_name_en VARCHAR(100),
    inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE dim_seller (
    seller_key BIGINT PRIMARY KEY,
    seller_id VARCHAR(50) NOT NULL,
    seller_state VARCHAR(2),
    inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE NOT NULL,
    month INT,
    quarter INT,
    year INT,
    inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================
-- C. KHỞI TẠO FACTS (Có cột Audit & Foreign Keys)
-- ==========================================
CREATE TABLE fact_orders (
    order_id VARCHAR(50) PRIMARY KEY,
    customer_key BIGINT REFERENCES dim_customer(customer_key),
    date_key INT REFERENCES dim_date(date_key),
    order_status VARCHAR(20),
    delivery_lead_time_days INT,
    is_late BOOLEAN,
    inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE fact_order_items (
    order_id VARCHAR(50) REFERENCES fact_orders(order_id),
    order_item_id INT,
    product_key BIGINT REFERENCES dim_product(product_key),
    seller_key BIGINT REFERENCES dim_seller(seller_key),
    date_key INT REFERENCES dim_date(date_key),
    price DOUBLE PRECISION,
    freight_value DOUBLE PRECISION,
    item_total_value DOUBLE PRECISION,
    inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (order_id, order_item_id)
);

CREATE TABLE fact_payment (
    order_id VARCHAR(50) REFERENCES fact_orders(order_id),
    payment_sequential INT,
    date_key INT REFERENCES dim_date(date_key),
    payment_type VARCHAR(20),
    payment_value DOUBLE PRECISION,
    inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (order_id, payment_sequential)
);

-- D. TỐI ƯU HÓA HIỆU NĂNG (INDEXING)
-- ==========================================
-- Partial Index: Chỉ lập chỉ mục cho các đơn hàng giao trễ
CREATE INDEX idx_fact_orders_late ON fact_orders(is_late) WHERE is_late = TRUE;