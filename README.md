# E-Commerce Returns & Profitability Intelligence Platform

An end-to-end data analytics and business intelligence project that analyzes e-commerce sales, product profitability, customer value, sales channel performance, and product returns using Python, PostgreSQL, SQL, and Power BI.

The project transforms raw e-commerce data into meaningful business insights through data auditing, preprocessing, database management, SQL analysis, and interactive dashboard development.

---

## 1. Project Overview

E-commerce businesses need to understand more than just their revenue. Product returns, refund amounts, customer purchasing behaviour, and product profitability also play an important role in business performance.

This project analyzes a synthetic global e-commerce dataset covering 2024–2026 to identify sales trends, profitability patterns, customer value, and return-related issues.

The final outcome is an interactive Power BI dashboard designed to help business stakeholders monitor key performance indicators and make data-driven decisions.

## 2. Project Objectives

- Analyze overall sales and revenue performance.
- Identify profitable products and loss-making transactions.
- Evaluate product return rates across categories.
- Identify the most common product return reasons.
- Analyze customer value and revenue contribution.
- Compare performance across different sales channels.
- Monitor order status and refund trends.
- Develop business KPIs and interactive visualizations.

## 3. Technology Stack

| Technology   | Purpose                                   |
| ------------ | ----------------------------------------- |
| Python       | Data cleaning and preprocessing           |
| Pandas       | Data manipulation and analysis            |
| NumPy        | Numerical operations                      |
| PostgreSQL   | Relational database management            |
| SQL          | Business analysis and data aggregation    |
| Power BI     | Interactive dashboard development         |
| pgAdmin 4    | PostgreSQL database management            |
| Git & GitHub | Version control and project documentation |

## 4. Dataset Description

**Dataset:** Global E-Commerce Orders & Returns 2024–2026

**Source:** [Prime Levels Data Hub](https://prime-levels.com/data-hub/global-ecommerce-orders-returns-2024-2026)

The dataset contains five CSV files:

| Dataset         | Records | Description                        |
| --------------- | ------: | ---------------------------------- |
| customers.csv   |   3,000 | Customer information               |
| orders.csv      |  14,000 | Order details and order status     |
| order_items.csv |  29,671 | Individual products purchased      |
| products.csv    |     345 | Product information and costs      |
| returns.csv     |   2,433 | Product returns and refund details |

**Dataset note:** The dataset is synthetic and intended for analytical and educational purposes. The findings represent the supplied dataset and should not be interpreted as actual company performance.

## 5. Project Workflow

The project follows an end-to-end data analytics workflow.

1. **Data Collection:** Obtained five CSV datasets.
2. **Data Auditing:** Checked missing values, duplicate records, foreign-key consistency, date formats, and financial calculations.
3. **Data Cleaning:** Used Python and Pandas to standardize date formats and prepare datasets.
4. **Database Development:** Created a PostgreSQL database and imported the cleaned datasets.
5. **SQL Analysis:** Performed joins, aggregations, profitability analysis, customer analysis, and return analysis.
6. **SQL Views:** Created nine analytical views for business reporting.
7. **Dashboard Development:** Connected PostgreSQL to Power BI and developed an interactive dashboard.
8. **Business Insights:** Analyzed sales performance, returns, customer value, and product profitability.

## 6. Database Structure

**Database Name:** `ecommerce_intelligence`

### Main Tables

- `customers`
- `orders`
- `order_items`
- `products`
- `returns`

### Analytical SQL Views

| View Name                      | Purpose                              |
| ------------------------------ | ------------------------------------ |
| `vw_business_kpis`             | Overall business performance metrics |
| `vw_category_return_analysis`  | Product category return analysis     |
| `vw_customer_value_analysis`   | Customer value and revenue analysis  |
| `vw_monthly_return_trend`      | Monthly returns and refund trends    |
| `vw_monthly_revenue_trend`     | Monthly delivered revenue trends     |
| `vw_order_status_analysis`     | Order status distribution            |
| `vw_product_profitability`     | Product-level profitability analysis |
| `vw_return_reason_analysis`    | Return reasons and refund analysis   |
| `vw_sales_channel_performance` | Sales channel performance            |

## 7. Key Business KPIs

The following metrics were verified using PostgreSQL.

| Business Metric     |        Result |
| ------------------- | ------------: |
| Total Orders        |        14,000 |
| Delivered Orders    |        12,030 |
| Cancelled Orders    |           807 |
| Delivered Revenue   | $6,842,340.19 |
| Average Order Value |       $568.77 |
| Delivered Profit    | $2,080,056.63 |
| Total Returns       |         2,433 |
| Total Refund Amount |   $410,427.05 |

## 8. Power BI Dashboard

The interactive Power BI dashboard provides an overview of business performance through KPI cards and analytical charts.

### Business Performance

- Total Delivered Revenue
- Total Delivered Orders
- Total Delivered Profit
- Total Refund Amount
- Total Returns

### Revenue Analysis

- Monthly Delivered Revenue Trend
- Revenue by Sales Channel
- Orders by Sales Channel

### Product Profitability

- Top 10 Products by Profit
- Profit by Product Category

### Returns Analysis

- Monthly Refund Amount Trend
- Returns by Reason
- Returns by Product Category
- Return Rate by Product Category

### Customer Analysis

- Top 10 Customers by Revenue

### Order Analysis

- Order Status Distribution

## 9. Key Business Insights

The SQL analysis identified the following findings:

**Order Performance**

- 12,030 orders were delivered.
- 807 orders were cancelled.
- Delivered orders account for approximately 85.93% of all orders.

**Revenue and Profitability**

- Delivered revenue exceeded $6.84 million.
- Delivered profit was approximately $2.08 million.
- Overall order-item analysis identified 484 loss-making individual order items.

**Returns Analysis**

- A total of 2,433 returns were recorded.
- Total refunds amounted to $410,427.05.
- Wrong size or fit was the leading return reason, accounting for 719 returns.

**Category Analysis**

- Apparel recorded the highest category return rate in the all-order analysis, approximately 13.19%.
- Electronics generated the highest category revenue in the product profitability analysis.

*Note: Category return rates depend on the sales denominator and return population used in the SQL analysis. The denominator should be considered when interpreting return-rate comparisons.*

## 10. Project Folder Structure

```text
Ecommerce_Returns_Intelligence/
│
├── data/
│   ├── raw/
│   │   ├── customers.csv
│   │   ├── orders.csv
│   │   ├── order_items.csv
│   │   ├── products.csv
│   │   └── returns.csv
│   │
│   └── processed/
│       ├── customers.csv
│       ├── orders.csv
│       ├── order_items.csv
│       ├── products.csv
│       └── returns.csv
│
├── reports/
│   └── data_audit_report.txt
│
├── sql/
│   └── SQL analysis scripts
│
├── dashboard/
│   └── Ecommerce_Returns_Profitability_Dashboard.pbix
│
├── data_audit.py
├── prepare_customers_csv.py
├── prepare_orders_csv.py
├── prepare_order_items_csv.py
├── prepare_products_csv.py
├── prepare_returns_csv.py
│
└── README.md
```

## 11. How to Run the Project

### Prerequisites

- Python 3.x
- PostgreSQL
- pgAdmin 4
- Power BI Desktop

### Step 1: Clone the Repository

```bash
git clone https://github.com/saurabpal10-byte/ecommerce-returns-profitability-intelligence.git
```

### Step 2: Install Dependencies

```bash
pip install pandas numpy matplotlib seaborn scikit-learn
```

### Step 3: Prepare the Dataset

Place the five source CSV files inside the `data/raw/` directory.

Run the Python preprocessing scripts to generate cleaned datasets inside `data/processed/`.

### Step 4: Set Up PostgreSQL

Create the database:

```sql
CREATE DATABASE ecommerce_intelligence;
```

Create the five database tables, import the processed CSV files, and execute the SQL scripts to create the analytical views.

### Step 5: Connect Power BI

Connect Power BI Desktop to PostgreSQL.

Connection details:

- Server: `localhost:5432`
- Database: `ecommerce_intelligence`

Load the analytical views and open the Power BI dashboard.

## 12. Skills Demonstrated

- Data Cleaning and Preprocessing
- Data Auditing
- Exploratory Data Analysis
- SQL Joins and Aggregations
- Common Table Expressions (CTEs)
- Relational Database Management
- Business KPI Analysis
- Product Profitability Analysis
- Customer Value Analysis
- Return Rate Analysis
- Data Visualization
- Business Intelligence Reporting

## 13. Future Improvements

- Develop automated data refresh pipelines.
- Add customer retention and cohort analysis.
- Build predictive models for return-risk identification.
- Introduce sales and demand forecasting.
- Add more interactive dashboard filters.
- Develop automated business reporting.

## 14. Author

**Saurav Pal**

B.Tech – Information Science and Engineering

Interested in Data Analytics, Business Intelligence, and Data-Driven Decision Making.

---

*This project was developed as a portfolio project to demonstrate practical data analytics, SQL, database management, and business intelligence skills.*
