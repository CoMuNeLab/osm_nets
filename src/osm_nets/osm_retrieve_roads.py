"""Retrieve and merge road networks from OpenStreetMap data.

This script processes OSM data to extract road networks for European regions,
merging them into a unified dataset.
"""

from pathlib import Path

from osm_nets import osm, osm_utils

datapath = osm.DATA / Path("graphs_roads_EU")
datapath.mkdir(parents=True, exist_ok=True)

osm.logconfig.setup_logging("INFO")


def retrieve() -> None:
    """Retrieve road networks for all European countries.

    Processes each country, extracts road data, and saves to individual files.
    """
    countries = osm_utils.load_regions(grow_regions=0.1, test=False).sort_values(by="code")
    print(countries)

    for id, region in countries.iterrows():
        osm.log.info(f"{id}/{len(countries)}, {region['code']}")
        if isinstance(region["geometry"], str):
            osm.logging.info(region["geometry"])
        pl_path = datapath / f"graph_{region['code']}_roads.gpkg"

        if pl_path.is_file() and True:
            osm.log.warning(f"File {pl_path.name} already present.")
            continue
        else:
            pl = osm.osm_roads(
                region["geometry"],
                osm_dump_file="./EU_roads.gpkg",
                node_prefix=str(region["code"]) + "_",
            )
            if len(pl) > 0:
                pl.write(pl_path)


def merge():
    """Merge all individual country road networks into a single dataset.

    Combines all saved country networks into unified files for full and
    giant connected component (GCC) versions.
    """
    graph = None
    graphs = sorted(datapath.glob("graph_[A-Z]*_roads.gpkg"))
    for pl_path in graphs:
        print(pl_path)
        if graph is None:
            graph = osm.Graph.read(pl_path, node_index="NODE_ID").to_meters()
        else:
            graph = graph.merge(osm.Graph.read(pl_path, node_index="NODE_ID").to_meters(), tol=100)
    if graph is None:
        return
    graph = graph.to_degree()
    graph.write(datapath / "roads_merged_full.gpkg")
    graph = graph.largest_component()
    graph.write(datapath / "roads_merged_GCC.gpkg")


if __name__ == "__main__":
    retrieve()
    merge()
