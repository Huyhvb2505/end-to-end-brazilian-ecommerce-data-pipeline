with source as (
    select * from {{ source('raw', 'olist_order_payments_dataset') }}
),

renamed as (
    select
        order_id,
        cast(payment_sequential as integer) as payment_sequential,
        lower(trim(payment_type)) as payment_type,
        cast(payment_installments as integer) as payment_installments,
        cast(payment_value as numeric(10,2)) as payment_value,
        _ingested_at
    from source
)

select * from renamed