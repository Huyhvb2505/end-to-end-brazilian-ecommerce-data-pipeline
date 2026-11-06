with source as (
    select * from {{ source('raw', 'olist_orders_dataset') }}
),

renamed as (
    select
        order_id,
        customer_id,
        lower(trim(order_status)) as order_status,
        CAST(order_purchase_timestamp AS TIMESTAMP) as order_purchase_timestamp,
        CAST(order_approved_at AS TIMESTAMP) as order_approved_at,
        CAST(order_delivered_carrier_date AS TIMESTAMP) as order_delivered_carrier_date,
        CAST(order_delivered_customer_date AS TIMESTAMP) as order_delivered_customer_date,
        CAST(order_estimated_delivery_date AS TIMESTAMP) as order_estimated_delivery_date,
        _ingested_at
    from source
)

select * from renamed