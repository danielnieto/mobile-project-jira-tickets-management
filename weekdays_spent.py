from datetime import datetime, timedelta
import sys

INPUT_DATE_FORMAT = "%Y-%m-%d"
OUTPUT_DATE_FORMAT = "%A, %d %B %Y"


def calculate_weekdays(start_date, end_date):
    """
    Calculates the number of weekdays (Monday-Friday) between two
    date objects, inclusive of the start and end dates.
    """
    if start_date > end_date:
        raise ValueError("Start date cannot be later than end date")

    weekday_count = 0
    current_date = start_date

    while current_date <= end_date:
        if current_date.weekday() < 5:
            weekday_count += 1
        current_date += timedelta(days=1)

    return weekday_count


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"\nUsage: python {sys.argv[0]} YYYY-MM-DD YYYY-MM-DD", file=sys.stderr)
        print("Error: Please provide both a start and end date.", file=sys.stderr)
        sys.exit(1)

    try:
        start_date = datetime.strptime(sys.argv[1], INPUT_DATE_FORMAT).date()
        end_date = datetime.strptime(sys.argv[2], INPUT_DATE_FORMAT).date()
    except ValueError:
        print("\nError: Invalid date format.", file=sys.stderr)
        print("Please make sure you use the YYYY-MM-DD format.", file=sys.stderr)
        sys.exit(1)

    try:
        business_days = calculate_weekdays(start_date, end_date)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Start Date: {start_date.strftime(OUTPUT_DATE_FORMAT)}")
    print(f"End Date:   {end_date.strftime(OUTPUT_DATE_FORMAT)}")
    print(f"\nTotal weekdays (Mon-Fri) found: {business_days}")
