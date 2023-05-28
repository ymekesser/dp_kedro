from math import radians
import pandas as pd
from scipy.spatial import cKDTree
import logging

log = logging.getLogger(__name__)


def preprocess_feature_set(
    hdb_resale_prices: pd.DataFrame,
    hdb_address_geodata: pd.DataFrame,
    mrt_stations_geodata: pd.DataFrame,
    mall_geodata: pd.DataFrame,
) -> pd.DataFrame:
    df_feature_set = pd.merge(
        hdb_resale_prices,
        hdb_address_geodata,
        how="left",
        on=["block", "street_name"],
    )

    missing_latitude_count = df_feature_set["latitude"].isnull().sum()
    log.info(
        f"Number of rows with missing address location: {missing_latitude_count} out of {df_feature_set.shape[0]}"
    )
    df_feature_set = df_feature_set.dropna(subset=["latitude"])

    df_feature_set = _add_closest_mrt(df_feature_set, mrt_stations_geodata)
    df_feature_set = _add_closest_mall(df_feature_set, mall_geodata)
    df_feature_set = _add_distance_to_cbd(df_feature_set)

    return df_feature_set


def _add_closest_mrt(df_feature_set, df_mrt_stations):
    df_feature_set = _find_closest_location(
        df_feature_set, df_mrt_stations, "closest_mrt"
    )
    return df_feature_set


def _add_closest_mall(df_feature_set, df_mall_geodata):
    df_feature_set = _find_closest_location(
        df_feature_set, df_mall_geodata, "closest_mall"
    )

    return df_feature_set


def _add_distance_to_cbd(df_feature_set):
    cbd_location = pd.DataFrame.from_dict(
        {
            "latitude": [1.280602347559877],
            "longitude": [103.85040609311484],
            "name": "CBD",
        }
    )

    df_feature_set = _find_closest_location(df_feature_set, cbd_location, "cbd")

    return df_feature_set


def _find_closest_location(
    df_feature_set: pd.DataFrame, df_locations: pd.DataFrame, location_type: str
) -> pd.DataFrame:
    EARTH_RADIUS = 6371

    # Convert latitude and longitude to radians
    df_feature_set["latitude_rad"] = df_feature_set["latitude"].apply(radians)
    df_feature_set["longitude_rad"] = df_feature_set["longitude"].apply(radians)
    df_locations["latitude_rad"] = df_locations["latitude"].apply(radians)
    df_locations["longitude_rad"] = df_locations["longitude"].apply(radians)

    # Create a KDTree for the location dataframe
    location_tree = cKDTree(df_locations[["latitude_rad", "longitude_rad"]])

    # Query the KDTree for each point in the points dataframe
    distances, indices = location_tree.query(
        df_feature_set[["latitude_rad", "longitude_rad"]], k=1
    )

    # Get the closest entry from the location dataframe
    df_feature_set[f"{location_type}"] = df_locations.loc[indices, "name"].values  # type: ignore
    df_feature_set[f"distance_to_{location_type}"] = distances * EARTH_RADIUS * 1000

    # Drop the intermediate columns
    df_feature_set.drop(["latitude_rad", "longitude_rad"], axis=1, inplace=True)

    return df_feature_set
