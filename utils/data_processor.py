def _clean_product_name(name):
    # remove commas inside ProductName: Mouse,Wireless → MouseWireless
    return name.replace(",", "")

def _clean_number(num_str):
    # remove commas in numbers: "1,500" → "1500"
    return num_str.replace(",", "")

def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries.

    Returns a list of dicts with keys:
    ['TransactionID', 'Date', 'ProductID', 'ProductName',
     'Quantity', 'UnitPrice', 'CustomerID', 'Region']
    """
    transactions = []

    for line in raw_lines:
        parts = line.split("|")

        # Skip rows with incorrect number of fields
        if len(parts) != 8:
            continue

        (transaction_id,
         date_str,
         product_id,
         product_name,
         quantity_str,
         unit_price_str,
         customer_id,
         region) = parts

        # Handle commas in ProductName
        product_name = _clean_product_name(product_name)

        # Handle commas in numeric fields
        quantity_str = _clean_number(quantity_str)
        unit_price_str = _clean_number(unit_price_str)

        try:
            quantity = int(quantity_str)
            unit_price = float(unit_price_str)
        except ValueError:
            # skip rows where numeric conversion fails
            continue

        tran = {
            "TransactionID": transaction_id,
            "Date": date_str,
            "ProductID": product_id,
            "ProductName": product_name,
            "Quantity": quantity,
            "UnitPrice": unit_price,
            "CustomerID": customer_id,
            "Region": region,
        }
        transactions.append(tran)

    return transactions
def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters.

    Parameters:
    - transactions: list of transaction dictionaries
    - region: filter by specific region (optional)
    - min_amount: minimum transaction amount (Quantity * UnitPrice) (optional)
    - max_amount: maximum transaction amount (optional)

    Returns:
    (valid_transactions_list, invalid_count, filter_summary_dict)
    """
    valid = []
    invalid_count = 0

    # First: validate according to rules
    for t in transactions:
        # All required fields must be present and non-empty
        required_fields = ["TransactionID", "ProductID", "CustomerID", "Region"]
        if any((field not in t or t[field] in [None, ""]) for field in required_fields):
            invalid_count += 1
            continue

        # Quantity and UnitPrice must be > 0
        if t["Quantity"] <= 0 or t["UnitPrice"] <= 0:
            invalid_count += 1
            continue

        # TransactionID must start with 'T'
        if not str(t["TransactionID"]).startswith("T"):
            invalid_count += 1
            continue

        # ProductID must start with 'P'
        if not str(t["ProductID"]).startswith("P"):
            invalid_count += 1
            continue

        # CustomerID must start with 'C'
        if not str(t["CustomerID"]).startswith("C"):
            invalid_count += 1
            continue

        valid.append(t)

    total_input = len(transactions)

    # Show available regions and amount range BEFORE applying filters
    if valid:
        regions = sorted({t["Region"] for t in valid if t["Region"]})
        amounts = [t["Quantity"] * t["UnitPrice"] for t in valid]
        min_possible = min(amounts)
        max_possible = max(amounts)
        print("Available regions:", ", ".join(regions))
        print(f"Transaction amount range: {min_possible:.2f} to {max_possible:.2f}")
    else:
        print("No valid transactions to filter.")

    # Now apply filters
    filtered_by_region = 0
    filtered_by_amount = 0

    filtered = valid

    if region is not None:
        before = len(filtered)
        filtered = [t for t in filtered if t["Region"] == region]
        filtered_by_region = before - len(filtered)
        print(f"After region filter ({region}): {len(filtered)} records")

    if min_amount is not None or max_amount is not None:
        before = len(filtered)
        new_filtered = []
        for t in filtered:
            amount = t["Quantity"] * t["UnitPrice"]
            if min_amount is not None and amount < min_amount:
                continue
            if max_amount is not None and amount > max_amount:
                continue
            new_filtered.append(t)
        filtered = new_filtered
        filtered_by_amount = before - len(filtered)
        print(f"After amount filter: {len(filtered)} records")

    summary = {
        "total_input": total_input,
        "invalid": invalid_count,
        "filtered_by_region": filtered_by_region,
        "filtered_by_amount": filtered_by_amount,
        "final_count": len(filtered),
    }

    return filtered, invalid_count, summary
def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions.
    Returns: float (total sum of Quantity * UnitPrice)
    Example: 1548000.50
    """
    total = 0.0
    for t in transactions:
        total += t["Quantity"] * t["UnitPrice"]
    return total
def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date.
    Returns: dictionary sorted by date chronologically.
    Format: {'2024-12-01': {'revenue': 12345.0, 'transaction_count': 8, 'unique_customers': 6}, ...}
    """
    trends = {}
    
    for t in transactions:
        date = t["Date"]
        revenue = t["Quantity"] * t["UnitPrice"]
        customer = t["CustomerID"]
        
        if date not in trends:
            trends[date] = {"revenue": 0.0, "transaction_count": 0, "unique_customers": set()}
        
        trends[date]["revenue"] += revenue
        trends[date]["transaction_count"] += 1
        trends[date]["unique_customers"].add(customer)
    
    # Replace sets with counts and sort chronologically
    for date in trends:
        trends[date]["unique_customers"] = len(trends[date]["unique_customers"])
    
    # Sort by date (chronological)
    return dict(sorted(trends.items()))
def find_peak_sales_day(transactions):
    """
    Identifies the date with highest revenue.
    Returns: tuple(date, revenue, transaction_count)
    Example: ('2024-12-15', 15800.0, 12)
    """
    peak_date = None
    max_revenue = -1
    date_stats = {}
    
    for t in transactions:
        date = t["Date"]
        revenue = t["Quantity"] * t["UnitPrice"]
        
        if date not in date_stats:
            date_stats[date] = {"revenue": 0.0, "count": 0}
        
        date_stats[date]["revenue"] += revenue
        date_stats[date]["count"] += 1
    
    for date, stats in date_stats.items():
        if stats["revenue"] > max_revenue:
            max_revenue = stats["revenue"]
            peak_date = date
    
    if peak_date:
        return (peak_date, max_revenue, date_stats[peak_date]["count"])
    return None
def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns.
    Returns: dictionary of customer statistics, sorted by total_spent descending.
    """
    customer_stats = {}
    
    for t in transactions:
        customer = t["CustomerID"]
        product = t["ProductName"]
        revenue = t["Quantity"] * t["UnitPrice"]
        
        if customer not in customer_stats:
            customer_stats[customer] = {
                "total_spent": 0.0,
                "transaction_count": 0,
                "avg_order_value": 0.0,
                "products_bought": set()
            }
        
        customer_stats[customer]["total_spent"] += revenue
        customer_stats[customer]["transaction_count"] += 1
        customer_stats[customer]["products_bought"].add(product)
    
    # Calculate avg_order_value and convert sets to lists
    for customer in customer_stats:
        stats = customer_stats[customer]
        stats["avg_order_value"] = stats["total_spent"] / stats["transaction_count"]
        stats["products_bought"] = sorted(list(stats["products_bought"]))
    
    # Sort by total_spent descending
    return dict(sorted(customer_stats.items(), key=lambda x: x[1]["total_spent"], reverse=True))
def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold.
    Returns: list of tuples (ProductName, total_quantity, total_revenue)
    """
    product_stats = {}
    
    for t in transactions:
        product = t["ProductName"]
        quantity = t["Quantity"]
        revenue = quantity * t["UnitPrice"]
        
        if product not in product_stats:
            product_stats[product] = {"quantity": 0, "revenue": 0.0}
        
        product_stats[product]["quantity"] += quantity
        product_stats[product]["revenue"] += revenue
    
    # Sort by total_quantity descending, take top n
    sorted_products = sorted(product_stats.items(), 
                           key=lambda x: x[1]["quantity"], reverse=True)[:n]
    
    # Format as list of tuples
    return [(name, stats["quantity"], stats["revenue"]) 
            for name, stats in sorted_products]
def low_performing_products(transactions, threshold):
    """
    Identifies products with low sales.
    Returns: list of tuples sorted by total_quantity ascending.
    """
    product_stats = {}
    
    for t in transactions:
        product = t["ProductName"]
        quantity = t["Quantity"]
        revenue = quantity * t["UnitPrice"]
        
        if product not in product_stats:
            product_stats[product] = {"quantity": 0, "revenue": 0.0}
        
        product_stats[product]["quantity"] += quantity
        product_stats[product]["revenue"] += revenue
    
    # Find products with total_quantity < threshold
    low_performers = [(name, stats["quantity"], stats["revenue"]) 
                     for name, stats in product_stats.items() 
                     if stats["quantity"] < threshold]
    
    # Sort by total_quantity ascending
    return sorted(low_performers, key=lambda x: x[1])
def region_wise_sales(transactions):
    """
    Analyzes sales by region.
    Returns: dictionary with region statistics, sorted by total_sales descending.
    """
    region_stats = {}
    total_all_revenue = calculate_total_revenue(transactions)
    
    for t in transactions:
        region = t["Region"]
        revenue = t["Quantity"] * t["UnitPrice"]
        
        if region not in region_stats:
            region_stats[region] = {"total_sales": 0.0, "transaction_count": 0}
        
        region_stats[region]["total_sales"] += revenue
        region_stats[region]["transaction_count"] += 1
    
    # Calculate percentage of total sales
    for region in region_stats:
        stats = region_stats[region]
        stats["percentage"] = (stats["total_sales"] / total_all_revenue) * 100
    
    # Sort by total_sales descending
    return dict(sorted(region_stats.items(), key=lambda x: x[1]["total_sales"], reverse=True))
def create_product_mapping(api_products):
    """
    Creates a mapping of product numeric IDs to product info.
    api_products: list of product dicts from fetch_all_products().
    Returns: {id: {'title': ..., 'category': ..., 'brand': ..., 'rating': ...}, ...}
    """
    mapping = {}
    for p in api_products:
        pid = p.get("id")
        if pid is None:
            continue
        mapping[pid] = {
            "title": p.get("title"),
            "category": p.get("category"),
            "brand": p.get("brand"),
            "rating": p.get("rating"),
        }
    return mapping
import os

def save_enriched_data(enriched_transactions, filename="data/enriched_sales_data.txt"):
    """
    Saves enriched transactions back to a pipe-delimited file.
    Includes all original fields + API_Category, API_Brand, API_Rating, API_Match.
    Handles None values by writing empty strings.
    """
    # Ensure folder exists
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filepath = os.path.join(base_dir, filename)

    header_fields = [
        "TransactionID", "Date", "ProductID", "ProductName",
        "Quantity", "UnitPrice", "CustomerID", "Region",
        "API_Category", "API_Brand", "API_Rating", "API_Match"
    ]

    with open(filepath, mode="w", encoding="utf-8") as f:
        # Write header
        f.write("|".join(header_fields) + "\n")

        for t in enriched_transactions:
            row = []
            for field in header_fields:
                value = t.get(field, "")
                if value is None:
                    value = ""
                row.append(str(value))
            f.write("|".join(row) + "\n")

    print(f"Enriched data saved to {filepath}")
import re

def _extract_numeric_product_id(product_id):
    """
    Extracts numeric part from ProductID like 'P101' -> 101.
    Returns int or None.
    """
    match = re.search(r"(\d+)", str(product_id))
    if not match:
        return None
    return int(match.group(1))

def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product information.

    - Extract numeric ID from ProductID (P101 -> 101, P5 -> 5)
    - If ID exists in product_mapping, add:
        API_Category, API_Brand, API_Rating, API_Match=True
    - If not, set API_Match=False and others to None.
    Returns: list of enriched transaction dicts.
    Also writes to data/enriched_sales_data.txt via save_enriched_data().
    """
    enriched = []

    for t in transactions:
        # Copy original transaction so we don't modify input list directly
        new_t = t.copy()

        numeric_id = _extract_numeric_product_id(t.get("ProductID"))
        product_info = product_mapping.get(numeric_id)

        if product_info:
            new_t["API_Category"] = product_info.get("category")
            new_t["API_Brand"] = product_info.get("brand")
            new_t["API_Rating"] = product_info.get("rating")
            new_t["API_Match"] = True
        else:
            new_t["API_Category"] = None
            new_t["API_Brand"] = None
            new_t["API_Rating"] = None
            new_t["API_Match"] = False

        enriched.append(new_t)

    # Save to file as assignment requires
    save_enriched_data(enriched)

    return enriched
