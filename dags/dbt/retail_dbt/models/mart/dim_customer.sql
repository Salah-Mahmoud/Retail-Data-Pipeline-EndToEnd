with source as (
    select * from {{ ref('stg_customer') }}
)

select
    {{ dbt_utils.generate_surrogate_key(['s."CustomerID"']) }} as customer_key,
    s."CustomerID",
    s."FullName",
    s."Email",
    s."PhoneNumber",
    s."Address",
    s."City",
    s."State",
    s."Country",
    s."ZipCode"
from source s

{% if is_incremental() %}
where s."CustomerID" not in (
    select "CustomerID"
    from {{ this }}
    where {{ this }}."FullName" = s."FullName"
      and {{ this }}."Email" = s."Email"
      and {{ this }}."Address" = s."Address"
)
{% endif %}
