with staging as(
    select 
        p.product_id,
        p_eng.product_category_name_english,
        p.product_name_length,
        p.product_description_length,
        p.product_photos_qty,
        p.product_weight_g,
        p.product_length_cm,
        p.product_height_cm,
        p.product_width_cm
    from {{ ref('stg_olist_products') }} as p
    left join {{ ref('stg_product_category_name_translation') }} as p_eng
        on p.product_category_name = p_eng.product_category_name
)

select * from staging