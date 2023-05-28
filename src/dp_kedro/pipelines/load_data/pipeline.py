from kedro.pipeline import Pipeline, node, pipeline

from .nodes import (
    load_hdb_address_geodata,
    load_hdb_resale_prices,
    load_mall_geodata,
    load_mrt_geodata,
    load_mrt_stations,
)


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=load_hdb_resale_prices,
                inputs="staging_hdb_resale_prices",
                outputs="storage_hdb_resale_prices",
                name="load_hdb_resale_prices_node",
            ),
            node(
                func=load_mrt_stations,
                inputs="staging_mrt_stations",
                outputs="storage_mrt_stations",
                name="load_mrt_stations_node",
            ),
            node(
                func=load_mrt_geodata,
                inputs="staging_mrt_geodata",
                outputs="storage_mrt_geodata",
                name="load_mrt_geodata_node",
            ),
            node(
                func=load_mall_geodata,
                inputs="staging_mall_geodata",
                outputs="storage_mall_geodata",
                name="load_mall_geodata_node",
            ),
            node(
                func=load_hdb_address_geodata,
                inputs="staging_hdb_address_geodata",
                outputs="storage_hdb_address_geodata",
                name="load_hdb_address_geodata_node",
            ),
        ],
    )  # type: ignore
