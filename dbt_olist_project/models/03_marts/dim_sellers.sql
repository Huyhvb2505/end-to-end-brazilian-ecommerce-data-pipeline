with sellers as (
    select
        seller_id,
        seller_zip_code_prefix,
        seller_city,
        seller_state
    from {{ ref('stg_olist_sellers') }}
)
select * from sellers