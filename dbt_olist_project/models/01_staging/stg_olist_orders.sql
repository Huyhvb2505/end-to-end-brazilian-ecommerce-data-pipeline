with source as (
    select * from {{ source('raw', 'olist_orders_dataset') }}
),

renamed as (
    select
        order_id,
        customer_id,
        lower(trim(order_status)) as order_status,
        to_timestamp(order_purchase_timestamp, 'DD/MM/YYYY HH24:MI') as order_purchase_timestamp,
        to_timestamp(order_approved_at, 'DD/MM/YYYY HH24:MI') as order_approved_at,
        to_timestamp(order_delivered_carrier_date, 'DD/MM/YYYY HH24:MI') as order_delivered_carrier_date,
        to_timestamp(order_delivered_customer_date, 'DD/MM/YYYY HH24:MI') as order_delivered_customer_date,
        to_timestamp(order_estimated_delivery_date, 'DD/MM/YYYY HH24:MI') as order_estimated_delivery_date,
        _ingested_at
    from source
)

select * from renamed