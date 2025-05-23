with source as (
    select * from {{ ref('product') }}
)

select
    "ProductID",
    "ProductName",
    "Category",
    "Price",
    "UpdatedAt"
from source
