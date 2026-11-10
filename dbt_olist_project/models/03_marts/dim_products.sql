with products as (
    select *
    from {{ ref('int_products_english') }}
)

select * from products