with source as (
    select * from {{ ref('store') }}
)

select
    "StoreID",
    "StoreName",
    "StoreLocation",
    "StoreType",
    "OpeningDate",
    "ManagerName"
from source
