with source as (
    select * from {{ ref('customer') }}
)

select
    "CustomerID",
    coalesce("FirstName", '') || ' ' || coalesce("LastName", '')  as "FullName",
    "Email",
    "PhoneNumber",
    "Address",
    "City",
    "State",
    "Country",
    "ZipCode"::text
from source

