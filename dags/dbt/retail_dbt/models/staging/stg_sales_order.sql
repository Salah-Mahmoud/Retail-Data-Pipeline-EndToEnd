with source as (
    select * from {{ ref('orders') }}
)

select
    "OrderID",
    "CustomerID",
    "DateID",
    "PaymentMethodID",
    "ProductID",
    "PromotionID",
    "StoreID",
    "QuantitySold",
    "TotalSales",
    "DiscountAmount",
    "NetSales"
from source
