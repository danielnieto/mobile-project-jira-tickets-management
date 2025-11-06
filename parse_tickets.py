import pandas as pd
from enum import StrEnum
import sys


class Status(StrEnum):
    DONE = "Done"
    TODO = "To do"
    IN_PROGRESS = "In Progress"
    RFR = "RFR"
    OPEN = "Open"


class Col(StrEnum):
    ORIGINAL_ESTIMATE = "Original estimate"
    RESOLUTION = "Resolution"
    TIME_SPENT = "Time Spent"
    STATUS = "Statu"


def tickets_with_estimates(df: pd.DataFrame) -> pd.DataFrame:
    return df.query(f"`{Col.ORIGINAL_ESTIMATE}`.notna()")


def tickets_without_estimates(df: pd.DataFrame) -> pd.DataFrame:
    return df.query(f"`{Col.ORIGINAL_ESTIMATE}`.isna()")


def tickets_with_status(df: pd.DataFrame, status: Status) -> pd.DataFrame:
    return df.query(f'`{Col.STATUS}` == "{status}"')


def tickets_not_done(df: pd.DataFrame) -> pd.DataFrame:
    return df.query(f'`{Col.STATUS}` != "{Status.DONE}"')


def get_total_time_estimate(df: pd.DataFrame) -> int:
    return int(df[Col.ORIGINAL_ESTIMATE].sum())


def get_total_time_spent(df: pd.DataFrame) -> int:
    query = f'`{Col.TIME_SPENT}`.notna() and `{Col.RESOLUTION}` == "{Status.DONE}"'
    return int(df.query(query)[Col.TIME_SPENT].sum())


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"\nUsage: python {sys.argv[0]} path/to/file.csv", file=sys.stderr)
        print("Error: Please provide the CSV file to analyze.", file=sys.stderr)
        sys.exit(1)

    df = pd.read_csv(sys.argv[1])

    try:
        total = len(df)
        done = len(tickets_with_status(df, Status.DONE))
        not_done = len(tickets_not_done(df))
        open_status = len(tickets_with_status(df, Status.OPEN))
        todo_status = len(tickets_with_status(df, Status.TODO))
        in_progress_status = len(tickets_with_status(df, Status.IN_PROGRESS))
        rfr_status = len(tickets_with_status(df, Status.RFR))
        with_estimates = len(tickets_with_estimates(df))
        without_estimates = len(tickets_without_estimates(df))
        total_estimation = get_total_time_estimate(df)
        total_spent = get_total_time_spent(df)
    except pd.errors.UndefinedVariableError as e:
        print(f"CSV format is not recognized: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Total tickets: {total}")
    print(f"Tickets done: {done}")
    print(f"Tickets not done: {not_done}")
    print(f"\tOpen: {open_status}")
    print(f"\tTo Do: {todo_status}")
    print(f"\tIn progress: {in_progress_status}")
    print(f"\tReady for review: {rfr_status}")
    print(f"Estimated tickets: {with_estimates}")
    print(f"Not yet estimated tickets: {without_estimates}")
    print(f"Total estimation: {total_estimation} seconds")
    print(f"Total time spent: {total_spent} seconds")
