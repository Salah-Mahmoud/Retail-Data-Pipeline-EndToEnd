with date_dimension as (
    select * from {{ ref('stg_date') }}
),
full_dt as (
    {{ dbt_date.get_base_dates(start_date="2018-01-01", end_date="2028-12-31") }}
),
full_dt_tr as (
    select
        {{ dbt_utils.generate_surrogate_key(['d."DateID"']) }} as date_key,
        d."DateID",
        d.date_day as Date,
        d.day_of_week_name as day,
        EXTRACT(MONTH FROM d.date_day) as month,
        EXTRACT(QUARTER FROM d.date_day) as quarter,
        EXTRACT(YEAR FROM d.date_day) as year
    from date_dimension d
    left join full_dt f on d.date_day = f.date_day
)
select
    date_key,
    "DateID",
    date,
    day,
    month,
    quarter,
    year
from full_dt_tr