from datetime import datetime

from dateutil.relativedelta import relativedelta


def get_next_bill_date(bill_date_str, bill_day):
    try:
        # Parse input bill date (YYYY-MM-DD format)
        bill_date = datetime.strptime(bill_date_str, "%Y-%m-%d")

        # Calculate the next month's bill date
        try:
            next_bill_date = bill_date.replace(day=bill_day, month=bill_date.month + 1)
        except ValueError:
            # If bill_day doesn't exist in the next month, use the last day
            next_month = bill_date + relativedelta(months=2)
            next_month = next_month.replace(day=1) - relativedelta(days=1)
            next_bill_date = next_month

        # Format output as YYYY-MM-DD
        return next_bill_date.strftime("%Y-%m-%d")

    except ValueError as e:
        return f"Error: Invalid date format. Use YYYY-MM-DD (e.g., 2025-01-31). {e}"

# # Example usage
# bill_date = "2025-01-31"  # Current bill date
# bill_day = 31  # Recurring bill day
#
# next_bill_date = get_next_bill_date(bill_date, bill_day)
# print(f"Bill Date: {bill_date}")
# print(f"Bill Day: {bill_day}")
# print(f"Next Bill Date: {next_bill_date}")
#
# # Test cases
# test_cases = [
#     ("2025-01-31", 31),  # Next: 2025-02-28
#     ("2025-06-15", 15),  # Next: 2025-07-15
#     ("2025-04-30", 30),  # Next: 2025-05-30
#     ("2025-12-31", 31)  # Next: 2026-01-31
# ]
#
# for bill_date, bill_day in test_cases:
#     print(f"\nBill Date: {bill_date}, Bill Day: {bill_day}")
#     print(f"Next Bill Date: {get_next_bill_date(bill_date, bill_day)}")
