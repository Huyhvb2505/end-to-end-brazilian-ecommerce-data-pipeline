with source as (
    select * from {{ source('raw', 'olist_geolocation_dataset') }}
),

cleaned as (
    select
        lpad(geolocation_zip_code_prefix::text, 5, '0') as geolocation_zip_code_prefix,
        cast(geolocation_lat as numeric(12, 8)) as geolocation_lat,
        cast(geolocation_lng as numeric(12, 8)) as geolocation_lng,
        initcap(trim(geolocation_city)) as geolocation_city,
        upper(trim(geolocation_state)) as geolocation_state,
        _ingested_at
    from source
)

select * from cleaned