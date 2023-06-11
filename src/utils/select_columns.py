import pandas as pd


def select_columns(df: pd.DataFrame, selector: dict) -> pd.DataFrame:
    return df.rename(columns=selector)[[*selector.values()]]
