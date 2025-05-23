{% snapshot dim_product %}
{{
    config(
        target_schema='dbt',
        strategy='timestamp',
        unique_key='"ProductID"',
        updated_at='"UpdatedAt"',
        invalidate_hard_deletes=True
    )
}}

select
    {{ dbt_utils.generate_surrogate_key(['"ProductID"']) }} as product_key,
    "ProductID",
    "ProductName",
    "Category",
    "Price",
    "UpdatedAt"
from {{ ref('stg_product') }}

{% endsnapshot %}