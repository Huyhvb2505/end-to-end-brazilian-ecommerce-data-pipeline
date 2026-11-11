with generated_dates as (
    {{ dbt_date.get_date_dimension("2016-01-01", "2018-12-31") }}
)
select
    date_day as full_date,
    day_of_week_name_short as day_of_week_name,
    day_of_month,
    month_name_short as month,
    -- quarter
    quarter_of_year,
    --year
    year_number as year
from generated_dates