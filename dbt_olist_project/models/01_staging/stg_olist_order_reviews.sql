with source as (
    select * from {{ source('raw', 'olist_order_reviews_dataset') }}
),

cleaned as (
    select
        review_id,
        order_id,
        cast(review_score as integer) as review_score,
        nullif(trim(review_comment_title), '') as review_comment_title,
        nullif(trim(review_comment_message), '') as review_comment_message,
        cast(review_creation_date as timestamp) as review_creation_date,
        cast(review_answer_timestamp as timestamp) as review_answer_timestamp,
        _ingested_at
    from source
)

select * from cleaned