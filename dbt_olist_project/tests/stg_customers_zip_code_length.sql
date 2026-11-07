-- Kiểm tra xem có dòng nào ở bảng stg_olist_customers có độ dài khác 5 ký tự không
select
    customer_id,
    customer_zip_code_prefix,
    length(customer_zip_code_prefix) as zip_length
from {{ ref('stg_olist_customers') }}
where length(customer_zip_code_prefix) != 5
   or customer_zip_code_prefix is null