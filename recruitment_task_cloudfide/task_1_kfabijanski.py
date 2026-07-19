import pandas as pd
import re

from cloudfide_recruitment_task import add_virtual_column

def dataframe_choice():
    # Example input DataFrame
    df = pd.DataFrame({
        "name": ["banana", "apple"],
        "quantity": [10, 3],
        "price": [10, 1]
    })
    # Example input DataFrame - wrong
    wrong_df = pd.DataFrame({
        "name": ["banana", "apple"],
        "q-x10": [10, 3],
        "price in USD": [10, 1]
    })

    while True:
        input_df = input("Do you want to use correct DataFrame? (y/n): ").strip().lower()
        if input_df in ['y', 'n']:
            break
        print("Choose 'y' or 'n'.")

    if input_df == 'y':
        return df
    elif input_df == 'n':
        return wrong_df

def is_valid_column_name(name: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z_]+", name))

def add_virtual_column(df: pd.DataFrame, role: str, new_column: str) -> pd.DataFrame:
    # 1. new_column validation
    if not is_valid_column_name(new_column):
        return pd.DataFrame()

    # 2. validation of existing columns
    for col in df.columns:
        if not is_valid_column_name(col):
            return pd.DataFrame()

    # 3. role cleaning
    role = role.strip()

    # only allowed chars
    if not re.fullmatch(r"[A-Za-z_+\-* ]+", role):
        return pd.DataFrame()

    # split (handles no spaces)
    tokens = re.split(r"(\+|\-|\*)", role.replace(" ", ""))

    #  should be: col op col
    if len(tokens) != 3:
        return pd.DataFrame()

    left, op, right = tokens

    # 4. validation of columns in role
    if left not in df.columns or right not in df.columns:
        return pd.DataFrame()

    # 5. execution of operation
    try:
        if op == "+":
            result = df[left] + df[right]
        elif op == "-":
            result = df[left] - df[right]
        elif op == "*":
            result = df[left] * df[right]
        else:
            return pd.DataFrame()
    except:
        return pd.DataFrame()

    # 6. return new df
    new_df = df.copy()
    new_df[new_column] = result

    return new_df

selected_df = dataframe_choice()
print("You selected DataFrame:")
print(selected_df)
print("Result of adding virtual column 'total_cost':")
print(add_virtual_column(selected_df, "quantity * price", "total_cost"))



