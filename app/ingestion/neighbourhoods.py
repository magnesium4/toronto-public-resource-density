from pathlib import Path
import geopandas as gpd


RAW_DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"
NEIGHBOURHOODS_FILE = RAW_DATA_DIR / "neighbourhoods.geojson"


# def load_neighbourhoods() -> list[dict]:
#     if not NEIGHBOURHOODS_FILE.exists():
#         raise FileNotFoundError(f"Neighbourhood file not found at {NEIGHBOURHOODS_FILE}")

#     with open(NEIGHBOURHOODS_FILE, "r", encoding="utf-8") as f:
#         geojson = json.load(f)

#     return geojson.get("features", [])


def load_neighbourhoods_with_area() -> gpd.GeoDataFrame:
    """
    Load neighbourhood polygons and compute area in square kilometers.
    """
    if not NEIGHBOURHOODS_FILE.exists():
        raise FileNotFoundError(
            f"Neighbourhood file not found at {NEIGHBOURHOODS_FILE}"
        )

    gdf = gpd.read_file(NEIGHBOURHOODS_FILE)

    # Reproject to a coordinate reference systems (CRS) suitable for Toronto (meters)
    # EPSG:26917 = NAD83 / UTM zone 17N
    gdf = gdf.to_crs(epsg=26917)

    # Compute area in square kilometers
    gdf["area_km2"] = gdf.geometry.area / 1_000_000

    return gdf