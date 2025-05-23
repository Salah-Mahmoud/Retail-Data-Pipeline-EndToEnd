{{ config(materialized='incremental', unique_key='"StoreID"') }}

with source as (
    select * from {{ ref('stg_store') }}
)

select
    {{ dbt_utils.generate_surrogate_key(['"StoreID"']) }} as store_key,
    *
from source

{% if is_incremental() %}
where "StoreID" not in (
    select "StoreID"
    from {{ this }}
    where {{ this }}."ManagerName" = source."ManagerName"
)
{% endif %}