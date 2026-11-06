with source as (
    select * from {{ source('raw', 'product_category_name_translation') }}
),

cleaned as (
    select
        trim(product_category_name) as product_category_name,
        trim(product_category_name_english) as product_category_name_english,
        _ingested_at
    from source
)

select * from cleaned