from kedro.pipeline import Pipeline, node, pipeline

from .nodes_hdb_resale_prices import preprocess_hdb_resale_prices
from .nodes_mrt_stations import preprocess_mrt_stations_with_geodata
from .nodes_malls import preprocess_malls_with_geodata
from .nodes_hdb_address import preprocess_addresses_with_geodata
from .node_feature_set import preprocess_feature_set


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=preprocess_hdb_resale_prices,
                inputs="storage_hdb_resale_prices",
                outputs="preprocessed_hdb_resale_prices",
                name="preprocess_hdb_resale_prices",
            ),
            node(
                func=preprocess_addresses_with_geodata,
                inputs="storage_hdb_address_geodata",
                outputs="preprocessed_hdb_address_geodata",
                name="preprocess_hdb_adress_geodata",
            ),
            node(
                func=preprocess_mrt_stations_with_geodata,
                inputs=["storage_mrt_stations", "storage_mrt_geodata"],
                outputs="preprocessed_mrt_stations_geodata",
                name="preprocess_mrt_stations_with_geodata",
            ),
            node(
                func=preprocess_malls_with_geodata,
                inputs="storage_mall_geodata",
                outputs="preprocessed_malls_geodata",
                name="preprocess_malls_geodata",
            ),
            node(
                func=preprocess_feature_set,
                inputs=[
                    "preprocessed_hdb_resale_prices",
                    "preprocessed_hdb_address_geodata",
                    "preprocessed_mrt_stations_geodata",
                    "preprocessed_malls_geodata",
                ],
                outputs="transformed_analytics_feature_set",
                name="preprocess_feature_set",
            ),
        ],
    )  # type: ignore
