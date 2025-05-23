{% snapshot dim_promotion %}
{{
    config(
        target_schema='dbt',
        strategy='timestamp',
        unique_key='"PromotionID"',
        updated_at='"UpdatedAt"',
        invalidate_hard_deletes=True
    )
}}

select
    {{ dbt_utils.generate_surrogate_key(['"PromotionID"']) }} as promotion_key,
    "PromotionID",
    "PromotionName",
    "DiscountPercentage",
    "PromotionType",
    "PromotionStartDate",
    "UpdatedAt"
from {{ ref('stg_promotion') }}

{% endsnapshot %}