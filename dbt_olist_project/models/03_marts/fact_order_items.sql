with order_items as (
    select
        order_id,
        product_id,
        seller_id,
        cast(shipping_limit_date as date) as shipping_limit_date,
        price,
        freight_value,
        (price + freight_value) as total_item
    from {{ ref('stg_olist_order_items') }}
)
select * from order_items