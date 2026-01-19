# main.py

import os
from utils.file_handler import read_sales_data
from utils.data_processor import (
    parse_transactions, validate_and_filter,
    calculate_total_revenue, daily_sales_trend, find_peak_sales_day,
    customer_analysis, top_selling_products, low_performing_products,
    region_wise_sales
)

def get_data_file():
    """Returns the path to the data file."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "data", "sales_data.txt")

def main():
    data_file = get_data_file()
    
    # Task 1 - Basic validation
    raw_lines = read_sales_data(data_file)
    transactions = parse_transactions(raw_lines)
    valid_transactions, invalid_count, summary = validate_and_filter(transactions)

    print(f"Total records parsed: {summary['total_input']}")
    print(f"Invalid records removed: {summary['invalid']}")
    print(f"Valid records after cleaning: {summary['final_count']}")

def test_part_2():
    """Test all Part 2 functions."""
    data_file = get_data_file()
    raw_lines = read_sales_data(data_file)
    transactions = parse_transactions(raw_lines)
    valid_transactions, _, _ = validate_and_filter(transactions)
    
    print("\n=== Part 2 Tests ===")
    
    # 2.1a
    total_rev = calculate_total_revenue(valid_transactions)
    print(f"Total Revenue: {total_rev}")
    
    # 2.2a
    trends = daily_sales_trend(valid_transactions)
    print(f"Daily Trends (first 3): {dict(list(trends.items())[:3])}")
    
    # 2.2b
    peak = find_peak_sales_day(valid_transactions)
    print(f"Peak Day: {peak}")
    
    # 2.2c (top 2 customers)
    customers = customer_analysis(valid_transactions)
    print(f"Top Customers (first 2): {dict(list(customers.items())[:2])}")
    
    # 2.2d
    top_products = top_selling_products(valid_transactions, n=3)
    print(f"Top 3 Products: {top_products}")
    
    # 2.3a (threshold=10)
    low_products = low_performing_products(valid_transactions, threshold=10)
    print(f"Low Performing (<10 qty): {low_products}")
    
    # 2.2e
    regions = region_wise_sales(valid_transactions)
    print(f"Region Sales: {regions}")

if __name__ == "__main__":
    main()
    test_part_2()

from utils.api_handler import fetch_all_products
from utils.data_processor import (
    # existing imports...
    create_product_mapping, enrich_sales_data
)
def test_part_3():
    """Tests API integration and enrichment."""
    data_file = get_data_file()
    raw_lines = read_sales_data(data_file)
    transactions = parse_transactions(raw_lines)
    valid_transactions, _, _ = validate_and_filter(transactions)

    print("\n=== Part 3: API Integration ===")

    api_products = fetch_all_products()
    if not api_products:
        print("No products fetched from API. Skipping enrichment test.")
        return

    product_mapping = create_product_mapping(api_products)
    print(f"Product mapping has {len(product_mapping)} entries.")

    enriched_transactions = enrich_sales_data(valid_transactions, product_mapping)
    print(f"Enriched {len(enriched_transactions)} transactions.")
    # Show first 2 for quick check
    for t in enriched_transactions[:2]:
        print(t)
if __name__ == "__main__":
    main()
    test_part_2()
    test_part_3()
# Final submission commit - all tasks complete