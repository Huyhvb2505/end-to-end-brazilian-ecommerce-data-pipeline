-- Kiểm tra tính duy nhất của khóa chính ( Lấy order_id kết hợp vs order_item_id làm
-- khóa chính)

select
    order_id,
    order_item_id,
    count(*) as record_count
from {{ref('stg_olist_order_items')}}
group by order_id, order_item_id
having count(*) > 1