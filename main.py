import sqlite3
import pandas as pd


# Підключення до початкової бази даних
connection = sqlite3.connect("data/shop.sqlite")

# Завантаження таблиць у DataFrame
products = pd.read_sql("SELECT * FROM products", connection)
sales = pd.read_sql("SELECT * FROM sales", connection)

connection.close()


print("Таблиця products:")
print(products)

print("\nТаблиця sales:")
print(sales)


# Об'єднання таблиць
df = sales.merge(
    products,
    left_on="product_id",
    right_on="id"
)

# Розрахунок суми кожного продажу
df["total_sales"] = df["quantity"] * df["price"]


# -------------------------------------------------
# product_statistics
# -------------------------------------------------

product_statistics = df.groupby(
    ["name", "category"],
    as_index=False
).agg(
    quantity_sold=("quantity", "sum"),
    total_sales=("total_sales", "sum")
)

print("\nProduct statistics:")
print(product_statistics)


# -------------------------------------------------
# category_statistics
# -------------------------------------------------

category_statistics = df.groupby(
    "category",
    as_index=False
).agg(
    operations=("id_x", "count"),
    quantity_sold=("quantity", "sum"),
    total_sales=("total_sales", "sum"),
    average_sale=("total_sales", "mean")
)

print("\nCategory statistics:")
print(category_statistics)


# -------------------------------------------------
# top_products
# -------------------------------------------------

top_products = product_statistics.sort_values(
    "quantity_sold",
    ascending=False
).head(5)

top_products = top_products[
    ["name", "category", "quantity_sold", "total_sales"]
]

print("\nTop products:")
print(top_products)


# -------------------------------------------------
# Збереження результатів у нову базу
# -------------------------------------------------

output_connection = sqlite3.connect(
    "output/shop_analysis.sqlite"
)

product_statistics.to_sql(
    "product_statistics",
    output_connection,
    if_exists="replace",
    index=False
)

category_statistics.to_sql(
    "category_statistics",
    output_connection,
    if_exists="replace",
    index=False
)

top_products.to_sql(
    "top_products",
    output_connection,
    if_exists="replace",
    index=False
)

output_connection.close()

print("\nАналіз завершено!")
print("Результати збережено в output/shop_analysis.sqlite")

