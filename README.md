# Sales Analytics System

Python system to clean, analyze, and enrich e-commerce sales data.

## Setup

1. Clone repository
2. `pip install -r requirements.txt`
3. Put `sales_data.txt` in `data/` folder

## Usage
```bash
python main.py

Features
Task 1: Data Cleaning
Handles encoding issues, removes commas
Validates TransactionID starts with T, Quantity>0, UnitPrice>0
Output: 80 total, 10 invalid, 70 valid

Task 2: Analytics
Total revenue, daily trends, peak sales day
Customer analysis, top/low performing products
Region-wise sales with percentages

Task 3: API Integration
Fetches products from DummyJSON API
Enriches with category/brand/rating
Saves data/enriched_sales_data.txt (12 columns)

Expected Output Files
data/enriched_sales_data.txt - 70 enriched transactions

## Expected Terminal Output
Total records parsed: 80
Invalid records removed: 10
Valid records after cleaning: 70
Total Revenue: 3527808.0
Fetched 100 products from DummyJSON API.
Enriched data saved to data/enriched_sales_data.txt
