with orders as (
    select
        order_id,
        customer_id,
        order_status,
        cast(order_purchase_timestamp as date) as order_date,
        cast(order_approved_at as date) as approved_date,
        cast(order_delivered_customer_date as date) as delivered_date,
        cast(order_estimated_delivery_date as date) as estimated_delivery_date
    from {{ ref('stg_olist_orders') }}
),
payments as (
    select
        *
    from {{ ref('int_order_payments_aggregated')}}
)
select
    o.order_id,
    o.customer_id,
    o.order_status,
    COALESCE(p.credit_card,0) as credit_card,
    COALESCE(p.boleto,0) as boleto,
    COALESCE(p.debit_card,0) as debit_card,
    COALESCE(p.voucher,0) as voucher,
    o.order_date,
    o.approved_date,
    o.delivered_date,
    o.estimated_delivery_date
from orders o left join payments p on o.order_id = p.order_id

select * from orders