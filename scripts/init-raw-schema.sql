-- Tạo schema raw nếu chưa tồn tại
CREATE SCHEMA IF NOT EXISTS raw;

-- 1. Customers (Khách hàng)
CREATE TABLE IF NOT EXISTS raw.olist_customers_dataset (
    customer_id VARCHAR(255),
    customer_unique_id VARCHAR(255),
    customer_zip_code_prefix VARCHAR(10),
    customer_city VARCHAR(100),
    customer_state VARCHAR(10),
    _ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Orders (Đơn hàng)
CREATE TABLE IF NOT EXISTS raw.olist_orders_dataset (
    order_id VARCHAR(255),
    customer_id VARCHAR(255),
    order_status VARCHAR(50),
    order_purchase_timestamp VARCHAR(50),
    order_approved_at VARCHAR(50),
    order_delivered_carrier_date VARCHAR(50),
    order_delivered_customer_date VARCHAR(50),
    order_estimated_delivery_date VARCHAR(50),
    _ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Order Items (Chi tiết sản phẩm trong đơn hàng)
CREATE TABLE IF NOT EXISTS raw.olist_order_items_dataset (
    order_id VARCHAR(255),
    order_item_id VARCHAR(50),
    product_id VARCHAR(255),
    seller_id VARCHAR(255),
    shipping_limit_date VARCHAR(50),
    price VARCHAR(50),
    freight_value VARCHAR(50),
    _ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Products (Sản phẩm)
CREATE TABLE IF NOT EXISTS raw.olist_products_dataset (
    product_id VARCHAR(255),
    product_category_name VARCHAR(255),
    product_name_lenght VARCHAR(50),
    product_description_lenght VARCHAR(50),
    product_photos_qty VARCHAR(50),
    product_weight_g VARCHAR(50),
    product_length_cm VARCHAR(50),
    product_height_cm VARCHAR(50),
    product_width_cm VARCHAR(50),
    _ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Sellers (Người bán)
CREATE TABLE IF NOT EXISTS raw.olist_sellers_dataset (
    seller_id VARCHAR(255),
    seller_zip_code_prefix VARCHAR(10),
    seller_city VARCHAR(100),
    seller_state VARCHAR(10),
    _ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. Order Payments (Thanh toán đơn hàng)
CREATE TABLE IF NOT EXISTS raw.olist_order_payments_dataset (
    order_id VARCHAR(255),
    payment_sequential VARCHAR(50),
    payment_type VARCHAR(50),
    payment_installments VARCHAR(50),
    payment_value VARCHAR(50),
    _ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 7. Order Reviews (Đánh giá đơn hàng)
CREATE TABLE IF NOT EXISTS raw.olist_order_reviews_dataset (
    review_id VARCHAR(255),
    order_id VARCHAR(255),
    review_score VARCHAR(50),
    review_comment_title TEXT,
    review_comment_message TEXT,
    review_creation_date VARCHAR(50),
    review_answer_timestamp VARCHAR(50),
    _ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 8. Geolocation (Thông tin địa lý/mã bưu chính)
CREATE TABLE IF NOT EXISTS raw.olist_geolocation_dataset (
    geolocation_zip_code_prefix VARCHAR(10),
    geolocation_lat VARCHAR(50),
    geolocation_lng VARCHAR(50),
    geolocation_city VARCHAR(100),
    geolocation_state VARCHAR(10),
    _ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 9. Product Category Name Translation (Dịch tên danh mục sản phẩm từ tiếng Bồ Đào Nha sang tiếng Anh)
CREATE TABLE IF NOT EXISTS raw.product_category_name_translation (
    product_category_name VARCHAR(255),
    product_category_name_english VARCHAR(255),
    _ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);