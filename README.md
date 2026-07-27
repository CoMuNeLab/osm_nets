# osm-retrieve-networks

A Python library for retrieving and processing network infrastructure data from OpenStreetMap.
This package provides tools to extract, clean, and analyze geographic networks including **railways**, **power lines**, and **road networks**.

## Features

- **Network Extraction**: Retrieve railway, power line, and road networks from OpenStreetMap data
- **Geographic Processing**: Clean and process geographic data with support for coordinate reference systems
- **Graph Operations**: Build and analyze network graphs with nodes and edges
- **Data Merging**: Combine networks from different regions or sources
- **Caching**: Built-in caching for OSM data to improve performance

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/CoMuNeLab/osm_nets.git
   cd osm_nets
   ```

2. Install the package using [uv](https://github.com/astral-sh/uv) (recommended):
   ```bash
   uv sync
   ```

   Or with pip:
   ```bash
   pip install -e .
   ```

## Usage

### Basic Example

```python
from pathlib import Path
import geopandas as gpd
from shapely import geometry
from osm_nets import osm_railways, osm_powerlines, osm_roads

# Define your area of interest (e.g., a polygon around a city)
place = geometry.Polygon([(20.0, 40.0), (20.1, 40.0), (20.1, 40.1), (20.0, 40.1)])

# Path to your OSM PBF dump file
osm_dump_file = Path("path/to/your/file.osm.pbf")

# Retrieve railway network
railway_graph = osm_railways(place, osm_dump_file)

# Retrieve power line network
powerline_graph, powerplants = osm_powerlines(place, osm_dump_file)

# Retrieve road network
road_graph = osm_roads(place, osm_dump_file)
```

### Working with PBF Files

The library includes utilities for extracting data from OSM PBF files:

```python
from osm_nets import pbf_extract

# Extract railway points (stations) and lines from PBF
stations = pbf_extract.extract_from_pbf("albania-latest.osm.pbf", kind="railway", geom="points")
lines = pbf_extract.extract_from_pbf("albania-latest.osm.pbf", kind="railway", geom="lines")
```

### Graph Operations

```python
# Save graph to file
railway_graph.write("railway_network.gpkg")

# Load graph from file
from osm_nets import Graph
loaded_graph = Graph.read("railway_network.gpkg")

# Get largest connected component
largest = railway_graph.largest_component()
```

### Example Notebook

See `examples/Example_railways.ipynb` for a complete walkthrough of retrieving and processing railway network data.

## Data Sources

You can download OSM PBF files from:
- [Geofabrik](https://download.geofabrik.de/) - Pre-processed extracts for countries and regions
- [OSMData](https://osmdata.openstreetmap.de/) - Custom extracts
- [Planet OSM](https://planet.osm.org/) - Full planet extracts

## Dependencies

- Python 3.12+
- geopandas
- osmnx
- igraph
- osmium
- shapely
- pyproj
- scipy
- tqdm
