with source as (
    select * from {{ ref('stg_payment') }}
)

select
      {{ dbt_utils.generate_surrogate_key(['"PaymentMethodID"']) }} as payment_key,
      *

from source
