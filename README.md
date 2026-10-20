# Olist E-Commerce End-to-End Data Engineering & Analytics Project

> **Prepared by:** Hager Abdelnasser (Data & AI Solutions Intern at HVIA)  
> **Tools & Technologies:** Python, Pandas, SQLAlchemy, SQL Server (SSMS), T-SQL, Power BI (DAX), Olist Public Dataset

---

## 📌 Project Overview
This project delivers an **end-to-end data engineering and analytics solution** built for **HVIA**, utilizing the Brazilian Olist e-commerce dataset (2016–2018). The pipeline covers the full data lifecycle: ingesting 9 raw datasets via an automated Python ETL script, transforming and modeling a structured **Star Schema** in SQL Server, enforcing referential integrity constraints, and building executive **Power BI dashboards** to uncover critical logistics and business insights.

---

## 🏗️ Technical Architecture & Workflow

### 1. Extract, Transform, Load (ETL Pipeline via Python)
* **Extract:** Automatically ingested 9 raw CSV tables (`customers`, `geolocation`, `order_items`, `payments`, `reviews`, `orders`, `products`, `sellers`, and category name translations) into dynamic Pandas DataFrames.
* **Transform:** 
  * Cleaned records by dropping duplicates and standardizing state abbreviations to uppercase.
  * Handled missing values (e.g., filling unknown product English categories).
  * Parsed raw timestamps into proper datetime formats (`pd.to_datetime`).
* **Load:** Established a secure connection using **SQLAlchemy** and **ODBC Driver**, successfully persisting dimension and fact tables into the `Olist_DW` database on SQL Server (`if_exists='replace'`).

### 2. Database Modeling & Constraints (SQL Server / SSMS)
* **Star Schema Design:** Structured the data warehouse around a central transaction table (`fact_order_items`) surrounded by clean dimensions (`dim_customers`, `dim_products`, `dim_sellers`, and separate date dimensions for purchase, approval, and delivery).
* **Data Integrity:** Enforced `PRIMARY KEY` and `FOREIGN KEY` constraints across tables to eliminate orphan records, guarantee referential integrity, and optimize analytical query performance.

### 3. Semantic Modeling & Visualization (Power BI & DAX)
* Established robust **one-to-many relationships** and star schema structures inside Power BI.
* Developed advanced **DAX measures** (utilizing `DATEDIFF`, `AVERAGEX`, and custom aggregations) to monitor total orders, sales volume, freight costs, and delivery durations.

---

## 📊 Key Findings & Business Insights

1. **The Growth Plateau (Finding 1):** Monthly orders surged from ~800 in early 2017 to over 7,500 during Black Friday (Nov 2017), before stabilizing between 6,200 and 7,300 through 2018, signaling a slowdown in compound user growth.
2. **The Delivery Satisfaction Cost (Finding 2):** 
   * Late deliveries (~8.1% of orders) are the primary driver of customer dissatisfaction.
   * On-time orders average a **4.29 review score**, whereas late orders plummet to **2.57** (with 54% receiving 1–2 stars).
   * Lateness spiked significantly during peak stress periods (e.g., 21.4% in March 2018).
3. **Geographic Bottlenecks (Finding 3):** While core activity centers around the Southeast (São Paulo accounts for 42% of customers and 64% of seller sales), northern and northeastern states suffer from severe delivery delays (e.g., Alagoas averages 24 days with a 24% late rate).
4. **Seller Concentration & Retention (Finding 4 & 5):** 
   * The top 10% of sellers generate 67% of total sales, while the median seller earned only ~R$824, exposing a large inactive long-tail and high concentration risk.
   * Customer retention is extremely low at **3.1% repeat purchase rate**, proving growth relies entirely on costly acquisition rather than loyalty.
5. **Freight Impact (Finding 6):** Freight consumes ~16.6% of item value overall, scaling up to 24% for bulky categories like furniture and decor.

---

## 💡 Strategic Solutions Proposed for HVIA

Based on the empirical findings, the following scalable data-driven solutions were proposed:

* **Delivery Risk & Promise Engine (Logistics Intelligence):** Build a predictive machine learning model at checkout/dispatch using route, weight, season, and seller history to dynamically predict delivery probabilities, update customer expectations, and issue early alerts for at-risk orders.
* **Seller Health & Scoring System:** Implement scoring models targeting the long tail for activation and top-tier sellers for retention, tying directly into credit-risk assessment frameworks.
* **Customer Segmentation & Pricing Optimization:** Deploy segmentation models to tackle the 3% repeat rate and guide category-specific freight strategies.

---

## 🛠️ How to Run the Project
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/hager-abdelnasser/Olist-Data-Engineering-Analytics.git](https://github.com/hager-abdelnasser/Olist-Data-Engineering-Analytics.git)
