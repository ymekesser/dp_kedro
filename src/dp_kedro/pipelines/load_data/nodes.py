from typing import Any
import pandas as pd


def load_hdb_resale_prices(hdb_resale_prices: pd.DataFrame) -> pd.DataFrame:
    return hdb_resale_prices


def load_mrt_stations(mrt_stations: pd.DataFrame) -> pd.DataFrame:
    return mrt_stations


def load_mrt_geodata(mrt_geodata: Any) -> pd.DataFrame:
    return _convert_overpass_json_to_dataframe(mrt_geodata)


def load_mall_geodata(mall_geodata: Any) -> pd.DataFrame:
    return _convert_overpass_json_to_dataframe(mall_geodata)


def load_hdb_address_geodata(hdb_address_geodata: pd.DataFrame) -> pd.DataFrame:
    return hdb_address_geodata


def _convert_overpass_json_to_dataframe(data: Any):
    data_dict = pd.json_normalize(data, record_path=["elements"])
    return pd.DataFrame.from_dict(data_dict, orient="columns")  # type: ignore
