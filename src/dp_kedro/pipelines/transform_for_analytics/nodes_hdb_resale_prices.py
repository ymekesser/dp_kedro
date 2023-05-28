import pandas as pd

from utils.select_columns import select_columns


def preprocess_hdb_resale_prices(hdb_resale_prices: pd.DataFrame) -> pd.DataFrame:
    hdb_resale_prices = _get_remaining_lease_in_months(hdb_resale_prices)
    hdb_resale_prices = _get_storey_median(hdb_resale_prices)
    hdb_resale_prices = _get_rooms(hdb_resale_prices)

    return select_columns(
        hdb_resale_prices,
        {
            "town": "town",
            "block": "block",
            "street_name": "street_name",
            "storey_median": "storey_median",
            "floor_area_sqm": "floor_area_sqm",
            "room_no": "room_no",
            "flat_model": "flat_model",
            "lease_commence_date": "lease_commence_date",
            "remaining_lease_in_months": "remaining_lease_in_months",
            "resale_price": "resale_price",
        },
    )


def _get_remaining_lease_in_months(hdb_resale_prices: pd.DataFrame) -> pd.DataFrame:
    hdb_resale_prices["remaining_lease_in_months"] = hdb_resale_prices[
        "remaining_lease"
    ].apply(_parse_duration)

    return hdb_resale_prices


def _parse_duration(duration_string: str) -> int:
    # Remaining lease always follows the same pattern,
    # either e.g. 56 years 09 months
    # or e.g. 63 years
    parts = duration_string.split()

    years = int(parts[0])
    months = int(parts[2]) if len(parts) > 2 else 0

    return years * 12 + months


def _get_storey_median(hdb_resale_prices: pd.DataFrame) -> pd.DataFrame:
    hdb_resale_prices["storey_median"] = hdb_resale_prices["storey_range"].apply(
        _calculate_median
    )

    return hdb_resale_prices


def _calculate_median(storey_range: str) -> int:
    # Floor level is given as a range, e.g. "10 TO 12"
    # To simplify, we take the Median

    [lower, upper] = map(int, storey_range.split(" TO "))

    return (lower + upper) // 2


def _get_rooms(hdb_resale_prices: pd.DataFrame) -> pd.DataFrame:
    hdb_resale_prices["room_no"] = hdb_resale_prices["flat_type"].apply(_parse_rooms)

    return hdb_resale_prices


def _parse_rooms(flat_type: str) -> int:
    # Flat time indicates number of rooms, e.g. "3 Room"
    # "Executive" flats have 5 rooms plus a study which we treat as an additional room
    # "Multi-Generation" flats have 6 rooms as well

    if flat_type == "EXECUTIVE" or flat_type == "MULTI-GENERATION":
        return 6

    split = flat_type.split()
    rooms_no = int(split[0])

    return rooms_no