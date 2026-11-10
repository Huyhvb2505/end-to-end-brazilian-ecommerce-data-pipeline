{% test row_count_match(model, raw_source_name, raw_table_name, tolerance_percent=0) %}

    with raw_count as (
        select count(*) as cnt 
        from {{ source(raw_source_name, raw_table_name) }}
    ),

    stg_count as (
        select count(*) as cnt 
        from {{ model }}
    )

    select 
        raw_count.cnt as raw_rows,
        stg_count.cnt as stg_rows,
        abs(raw_count.cnt - stg_count.cnt) as diff_rows
    from raw_count, stg_count
    -- Báo lỗi (Fail) nếu số dòng lệch nhau khác 0 (hoặc vượt ngưỡng cho phép)
    where abs(raw_count.cnt - stg_count.cnt) > {{ tolerance_percent }}

{% endtest %}