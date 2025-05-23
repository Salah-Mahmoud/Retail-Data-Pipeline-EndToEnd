with source as (
    select * from {{ ref('stg_sales_order') }}
)

select
    {{ dbt_utils.generate_surrogate_key(['"OrderID"']) }} as sales_key,
    {{ dbt_utils.generate_surrogate_key(['"ProductID"']) }} as product_key,
    {{ dbt_utils.generate_surrogate_key(['"CustomerID"']) }} as customer_key,
    {{ dbt_utils.generate_surrogate_key(['"PaymentMethodID"']) }} as payment_key,
    {{ dbt_utils.generate_surrogate_key(['"DateID"']) }} as date_key,
    {{ dbt_utils.generate_surrogate_key(['"PromotionID"']) }} as promotion_key,
    {{ dbt_utils.generate_surrogate_key(['"StoreID"']) }} as store_key,
    "QuantitySold",
    "TotalSales",
    "DiscountAmount",
    "NetSales"
from source


