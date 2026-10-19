import urllib
import pandas as pd
from sqlalchemy import create_engine, text

# 1. Define File Paths
file_paths = {
    "customers": "C:/HVIA_Internship/Tasks/TASK 1_New Ver/archive/olist_customers_dataset.csv",
    "geolocation": "C:/HVIA_Internship/Tasks/TASK 1_New Ver/archive/olist_geolocation_dataset.csv",
    "order_items": "C:/HVIA_Internship/Tasks/TASK 1_New Ver/archive/olist_order_items_dataset.csv",
    "order_payments": "C:/HVIA_Internship/Tasks/TASK 1_New Ver/archive/olist_order_payments_dataset.csv",
    "order_reviews": "C:/HVIA_Internship/Tasks/TASK 1_New Ver/archive/olist_order_reviews_dataset.csv",
    "orders": "C:/HVIA_Internship/Tasks/TASK 1_New Ver/archive/olist_orders_dataset.csv",
    "products": "C:/HVIA_Internship/Tasks/TASK 1_New Ver/archive/olist_products_dataset.csv",
    "sellers": "C:/HVIA_Internship/Tasks/TASK 1_New Ver/archive/olist_sellers_dataset.csv",
    "category_translation": "C:/HVIA_Internship/Tasks/TASK 1_New Ver/archive/product_category_name_translation.csv",
}

# Load all datasets into a dictionary of DataFrames
dfs = {name: pd.read_csv(path) for name, path in file_paths.items()}

# 2. Data Cleaning
dfs["customers"] = dfs["customers"].drop_duplicates()
dfs["customers"]["customer_state"] = dfs["customers"][
    "customer_state"
].str.upper()

dfs["sellers"] = dfs["sellers"].drop_duplicates()
dfs["sellers"]["seller_state"] = dfs["sellers"]["seller_state"].str.upper()

# Clean Geolocation dataset (dropping duplicates and standardizing state names)
dfs["geolocation"] = dfs["geolocation"].drop_duplicates()
if "geolocation_state" in dfs["geolocation"].columns:
    dfs["geolocation"]["geolocation_state"] = dfs["geolocation"][
        "geolocation_state"
    ].str.upper()

# Handle date conversions for orders
date_cols = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]
for col in date_cols:
  if col in dfs["orders"].columns:
    dfs["orders"][col] = pd.to_datetime(dfs["orders"][col], errors="coerce")

# Merge products with English category translation
products_df = dfs["products"].drop_duplicates()
translation_df = dfs["category_translation"]
products_df = products_df.merge(
    translation_df, on="product_category_name", how="left"
)
products_df["product_category_name_english"] = products_df[
    "product_category_name_english"
].fillna("Unknown")

# 3. Building the Star Schema with Separate Date Dimensions
dim_customers = dfs["customers"][
    ["customer_id", "customer_unique_id", "customer_city", "customer_state"]
].drop_duplicates()

dim_products = products_df[[
    "product_id",
    "product_category_name_english",
    "product_weight_g",
    "product_length_cm",
    "product_height_cm",
    "product_width_cm",
]].rename(columns={"product_category_name_english": "product_category"}).drop_duplicates()

dim_sellers = dfs["sellers"][
    ["seller_id", "seller_city", "seller_state"]
].drop_duplicates()

# Build Geolocation Dimension
dim_geolocation = dfs["geolocation"][[
    "geolocation_zip_code_prefix",
    "geolocation_lat",
    "geolocation_lng",
    "geolocation_city",
    "geolocation_state",
]].drop_duplicates()


# --- Helper Function to Create Separate Date Dimensions ---
def create_date_dimension(date_series):
  d_df = pd.DataFrame({"date_id": date_series.dt.date.dropna().unique()})
  d_df["date_id"] = pd.to_datetime(d_df["date_id"])
  d_df["year"] = d_df["date_id"].dt.year
  d_df["month"] = d_df["date_id"].dt.month
  d_df["day"] = d_df["date_id"].dt.day
  d_df["day_of_week"] = d_df["date_id"].dt.day_name()
  return d_df.drop_duplicates().reset_index(drop=True)


dim_purchase_date = create_date_dimension(
    dfs["orders"]["order_purchase_timestamp"]
)
dim_approved_date = create_date_dimension(dfs["orders"]["order_approved_at"])
dim_delivery_date = create_date_dimension(
    dfs["orders"]["order_delivered_customer_date"]
)

# --- Fact Table ---
orders_subset = dfs["orders"][[
    "order_id",
    "customer_id",
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_customer_date",
]].copy()

orders_subset["purchase_date"] = orders_subset[
    "order_purchase_timestamp"
].dt.date
orders_subset["approved_date"] = orders_subset["order_approved_at"].dt.date
orders_subset["delivered_customer_date"] = orders_subset[
    "order_delivered_customer_date"
].dt.date

fact_order_items = dfs["order_items"].drop_duplicates()
fact_order_items = fact_order_items.merge(
    orders_subset[[
        "order_id",
        "customer_id",
        "purchase_date",
        "approved_date",
        "delivered_customer_date",
    ]],
    on="order_id",
    how="inner",
)

fact_order_items = fact_order_items[[
    "order_id",
    "order_item_id",
    "product_id",
    "seller_id",
    "customer_id",
    "purchase_date",
    "approved_date",
    "delivered_customer_date",
    "price",
    "freight_value",
]].drop_duplicates()

server_name = r".\SQLEXPRESS01"
database_name = "Olist_DW2"

params = urllib.parse.quote_plus(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={server_name};"
    f"DATABASE={database_name};"
    f"Trusted_connection=yes;"
    f"TrustServerCertificate=yes;"
)
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

with engine.begin() as conn:
  conn.execute(text("DROP TABLE IF EXISTS fact_order_items"))
  conn.execute(text("DROP TABLE IF EXISTS dim_purchase_date"))
  conn.execute(text("DROP TABLE IF EXISTS dim_approved_date"))
  conn.execute(text("DROP TABLE IF EXISTS dim_delivery_date"))
  conn.execute(text("DROP TABLE IF EXISTS dim_customers"))
  conn.execute(text("DROP TABLE IF EXISTS dim_products"))
  conn.execute(text("DROP TABLE IF EXISTS dim_sellers"))
  conn.execute(text("DROP TABLE IF EXISTS dim_geolocation"))

print("Uploading Dimension Tables...")
dim_customers.to_sql("dim_customers", engine, if_exists="replace", index=False)
dim_products.to_sql("dim_products", engine, if_exists="replace", index=False)
dim_sellers.to_sql("dim_sellers", engine, if_exists="replace", index=False)
dim_geolocation.to_sql(
    "dim_geolocation",
    engine,
    if_exists="replace",
    index=False,
    chunksize=10000,
)

dim_purchase_date.to_sql(
    "dim_purchase_date", engine, if_exists="replace", index=False
)
dim_approved_date.to_sql(
    "dim_approved_date", engine, if_exists="replace", index=False
)
dim_delivery_date.to_sql(
    "dim_delivery_date", engine, if_exists="replace", index=False
)

print(
    "Uploading Fact Table (this may take a few seconds due to size)..."
)
fact_order_items.to_sql(
    "fact_order_items",
    engine,
    if_exists="replace",
    index=False,
    chunksize=10000,
)

print("ETL Pipeline completed successfully in Olist_DW2 with Geolocation!")