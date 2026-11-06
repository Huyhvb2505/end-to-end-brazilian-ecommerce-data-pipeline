with source as (
    select * from {{ source('raw', 'olist_sellers_dataset') }}
),

renamed as (
    select
        seller_id,
        lpad(seller_zip_code_prefix::text, 5, '0') as seller_zip_code_prefix,
        initcap(trim(seller_city)) as seller_city,
        upper(trim(seller_state)) as seller_state,
        _ingested_at
    from source
)

select * from renamed