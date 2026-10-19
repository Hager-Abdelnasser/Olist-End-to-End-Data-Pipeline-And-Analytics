USE Olist_DW2;

ALTER TABLE dim_customers ALTER COLUMN customer_id VARCHAR(255) NOT NULL;
ALTER TABLE dim_customers ADD CONSTRAINT PK_dim_customers PRIMARY KEY (customer_id);

ALTER TABLE dim_products ALTER COLUMN product_id VARCHAR(255) NOT NULL;
ALTER TABLE dim_products ADD CONSTRAINT PK_dim_products PRIMARY KEY (product_id);

ALTER TABLE dim_sellers ALTER COLUMN seller_id VARCHAR(255) NOT NULL;
ALTER TABLE dim_sellers ADD CONSTRAINT PK_dim_sellers PRIMARY KEY (seller_id);

ALTER TABLE dim_purchase_date ALTER COLUMN date_id DATE NOT NULL;
ALTER TABLE dim_purchase_date ADD CONSTRAINT PK_dim_purchase_date PRIMARY KEY (date_id);

ALTER TABLE dim_approved_date ALTER COLUMN date_id DATE NOT NULL;
ALTER TABLE dim_approved_date ADD CONSTRAINT PK_dim_approved_date PRIMARY KEY (date_id);

ALTER TABLE dim_delivery_date ALTER COLUMN date_id DATE NOT NULL;
ALTER TABLE dim_delivery_date ADD CONSTRAINT PK_dim_delivery_date PRIMARY KEY (date_id);

ALTER TABLE fact_order_items ALTER COLUMN customer_id VARCHAR(255) NULL;
ALTER TABLE fact_order_items ALTER COLUMN product_id VARCHAR(255) NULL;
ALTER TABLE fact_order_items ALTER COLUMN seller_id VARCHAR(255) NULL;
ALTER TABLE fact_order_items ALTER COLUMN purchase_date DATE NULL;
ALTER TABLE fact_order_items ALTER COLUMN approved_date DATE NULL;
ALTER TABLE fact_order_items ALTER COLUMN delivered_customer_date DATE NULL;

ALTER TABLE fact_order_items ADD CONSTRAINT FK_fact_customer FOREIGN KEY (customer_id) REFERENCES dim_customers(customer_id);
ALTER TABLE fact_order_items ADD CONSTRAINT FK_fact_product FOREIGN KEY (product_id) REFERENCES dim_products(product_id);
ALTER TABLE fact_order_items ADD CONSTRAINT FK_fact_seller FOREIGN KEY (seller_id) REFERENCES dim_sellers(seller_id);

ALTER TABLE fact_order_items ADD CONSTRAINT FK_fact_purchase_date FOREIGN KEY (purchase_date) REFERENCES dim_purchase_date(date_id);
ALTER TABLE fact_order_items ADD CONSTRAINT FK_fact_approved_date FOREIGN KEY (approved_date) REFERENCES dim_approved_date(date_id);
ALTER TABLE fact_order_items ADD CONSTRAINT FK_fact_delivery_date FOREIGN KEY (delivered_customer_date) REFERENCES dim_delivery_date(date_id);
