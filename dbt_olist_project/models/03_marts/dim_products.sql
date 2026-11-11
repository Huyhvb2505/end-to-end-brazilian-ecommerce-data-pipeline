with products as (
    select *
    from {{ ref('int_products_english') }}
)
select 
    product_id,
    COALESCE(product_category_name_english, 'Unknown') AS product_category_name_english
from products