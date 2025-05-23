with source as (
    select * from {{ ref('promotion') }}
)

select
    "PromotionID",
    "PromotionName",
    "DiscountPercentage",
    "PromotionType",
    "PromotionStartDate",
    "UpdatedAt"
from source
