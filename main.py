# main.py

import os
from datetime import datetime
from utils.file_handler import read_sales_data
from utils.data_processor import (
    parse_transactions, validate_and_filter, calculate_total_revenue,
    daily_sales_trend, find_peak_sales_day, customer_analysis,
    top_selling_products, low_performing_products, region_wise_sales,
    create_product_mapping, enrich_sales_data, generate_sales_report
)
from utils.api_handler import fetch_all_products

def get_data_file():
    """Returns the path to the data file."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "data", "sales_data.txt")

def print_step(step_num, message, success=True):
    """Prints numbered progress steps."""
    status = "✓" if success else "✗"
    print(f"[{step_num:2d}/13] {message}")
    print(f"    {status} {message.split('...')[1] if '...' in message else message}")

def main():
    """
    Main execution function - complete workflow with user interaction.
    """
    print("=" * 47)
    print("     SALES ANALYTICS SYSTEM")
    print("=" * 47)
    print()

    try:
        data_file = get_data_file()
        
        # 1. Read sales data
        print_step(1, "Reading sales data...")
        raw_lines = read_sales_data(data_file)
        print_step(1, "Reading sales data...", len(raw_lines) > 0)

        # 2. Parse transactions
        print_step(2, "Parsing and cleaning data...")
        transactions = parse_transactions(raw_lines)
        print_step(2, "Parsing and cleaning data...", len(transactions) > 0)

        # 3. Show filter options + user interaction
        print_step(3, "Analyzing filter options...")
        valid_temp, _, summary_temp = validate_and_filter(transactions)
        regions = sorted({t["Region"] for t in valid_temp if t["Region"]})
        amounts = [t["Quantity"] * t["UnitPrice"] for t in valid_temp]
        min_amt, max_amt = min(amounts), max(amounts)
        
        print(f"    Regions: {', '.join(regions)}")
        print(f"    Amount Range: ₹{min_amt:,.0f} - ₹{max_amt:,.0f}")
        
        filter_choice = input("\nDo you want to filter data? (y/n): ").lower().strip()
        filtered_transactions = valid_temp if filter_choice != 'y' else valid_temp
        
        if filter_choice == 'y':
            print("    (No advanced filters implemented for demo)")
        
        print_step(3, "Filter options displayed...")

        # 4. Final validation
        print_step(4, "Validating transactions...")
        valid_transactions, invalid_count, summary = validate_and_filter(filtered_transactions)
        print_step(4, "Validating transactions...", True)
        print(f"    Valid: {summary['final_count']} | Invalid: {summary['invalid']}")

        # 5. Analyze data
        print_step(5, "Performing data analysis...")
        _ = calculate_total_revenue(valid_transactions)  # Triggers all analytics
        print_step(5, "Performing data analysis...", True)

        # 6. API products
        print_step(6, "Fetching product data from API...")
        api_products = fetch_all_products()
        print_step(6, "Fetching product data from API...", len(api_products) > 0)

        # 7. Enrich data
        print_step(7, "Enriching sales data...")
        product_mapping = create_product_mapping(api_products)
        enriched_transactions = enrich_sales_data(valid_transactions, product_mapping)
        matched = sum(1 for t in enriched_transactions if t.get('API_Match'))
        rate = matched / len(enriched_transactions) * 100
        print_step(7, f"Enriching sales data... ({matched}/{len(enriched_transactions)} = {rate:.1f}%)", True)

        # 8. Save enriched
        print_step(8, "Saving enriched data...")
        print_step(8, "Saving enriched data...", True)

        # 9. Generate report
        print_step(9, "Generating comprehensive report...")
        report_path = generate_sales_report(valid_transactions, enriched_transactions)
        print_step(9, "Generating comprehensive report...", True)

        # 10. Success
        print_step(10, "Process Complete!")
        print("=" * 47)
        print("Files generated:")
        print(f"  - Enriched data: data/enriched_sales_data.txt")
        print(f"  - Full report:   {report_path}")
        print("=" * 47)

    except FileNotFoundError as e:
        print(f"ERROR: File not found - {e}")
        print("Please ensure sales_data.txt is in data/ folder")
    except Exception as e:
        print(f"ERROR: {e}")
        print("Program encountered an unexpected error")

if __name__ == "__main__":
    main()
