with source as (
    select * from {{ ref('payment') }}
)

select
    "PaymentMethodID",
    "PaymentType",
    "Provider"
from source


