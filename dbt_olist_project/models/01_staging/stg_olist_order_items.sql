with source as (
    select * from {{ source('raw', 'olist_order_items_dataset') }}
),

renamed as (
    select
        order_id as order_id,
        cast(order_item_id as integer) as order_item_id,
        product_id,
        seller_id,
        to_timestamp(shipping_limit_date, 'DD/MM/YYYY HH24:MI') as shipping_limit_date,
        cast(price as numeric(10,2)) as price,
        cast(freight_value as numeric(10,2)) as freight_value,
        _ingested_at
    from source
)

select * from renamed