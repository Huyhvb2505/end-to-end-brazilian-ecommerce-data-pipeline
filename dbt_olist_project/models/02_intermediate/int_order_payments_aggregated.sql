with payments as (
    select *
    from {{ ref('stg_olist_order_payments') }} 
)
select 
    order_id,
    sum(case when payment_type = 'boleto' then payment_value else 0 end) as boleto,
    sum(case when payment_type = 'credit_card' then payment_value else 0 end) as credit_card,
    sum(case when payment_type = 'debit_card' then payment_value else 0 end) as debit_card,
    sum(case when payment_type = 'voucher' then payment_value else 0 end) as voucher,
    sum(case when payment_type = 'not_defined' then payment_value else 0 end) as not_defined,
    max(payment_installments) as max_payment_installments
from payments 
group by order_id