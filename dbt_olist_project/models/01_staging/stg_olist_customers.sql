with source as (
    select * from {{ source('raw', 'olist_customers_dataset') }}
),

renamed as (
    select
        customer_id,
        customer_unique_id,
        lpad(customer_zip_code_prefix::text, 5, '0') as customer_zip_code_prefix,
        initcap(trim(customer_city)) as customer_city,
        upper(trim(customer_state)) as customer_state,
        _ingested_at
    from source
)

select * from renamed