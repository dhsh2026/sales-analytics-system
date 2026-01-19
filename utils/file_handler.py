def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues.

    Returns: list of raw lines (strings) WITHOUT header.
    Example: ['T001|2024-12-01|P101|Laptop|2|45000|C001|North', ...]
    """
    encodings_to_try = ["utf-8", "latin-1", "cp1252"]
    last_error = None
    lines = None

    for enc in encodings_to_try:
        try:
            with open(filename, mode="r", encoding=enc, errors="strict") as f:
                raw = f.readlines()
            lines = [line.strip() for line in raw if line.strip() != ""]
            break
        except (UnicodeDecodeError, FileNotFoundError) as e:
            last_error = e

    if lines is None:
        # If we are here, all decoding attempts failed OR file not found
        if isinstance(last_error, FileNotFoundError):
            print(f"Error: file '{filename}' not found.")
        else:
            print(f"Error reading file '{filename}': {last_error}")
        return []

    # Remove header row (first line)
    if lines:
        lines = lines[1:]

    return lines
