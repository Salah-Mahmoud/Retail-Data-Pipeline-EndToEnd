with date_dim as (

    {{ dbt_date.get_date_dimension("2018-01-01", "2028-12-31") }}

)

select
    *,
    'DATE_' || to_char(date_day, 'YYYYMMDD') as "DateID"
from date_dim
