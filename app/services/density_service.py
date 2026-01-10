import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

from app.ingestion.load_washrooms import load_geojson, parse_features
from app.ingestion.neighbourhoods import load_neighbourhoods_with_area


def compute_washroom_density() -> pd.DataFrame:
    """
    Compute washroom density per neighbourhood.
    """
    washrooms_df = parse_features(load_geojson())
    neighbourhoods_gdf = load_neighbourhoods_with_area()

    # Convert washrooms to GeoDataFrame
    geometry = [
        Point(lon, lat)
        for lon, lat in zip(washrooms_df["longitude"], washrooms_df["latitude"])
    ]

    washrooms_gdf = gpd.GeoDataFrame(
        washrooms_df.copy(),
        geometry=geometry,
        crs="EPSG:4326",
    ).to_crs(neighbourhoods_gdf.crs)

    # Spatial join
    joined = gpd.sjoin(
        washrooms_gdf,
        neighbourhoods_gdf,
        how="left",
        predicate="within",
    )

    density_df = (
        joined.groupby("AREA_NAME")
        .size()
        .reset_index(name="resource_count")
        .merge(
            neighbourhoods_gdf[["AREA_NAME", "area_km2"]],
            on="AREA_NAME",
            how="left",
        )
        .assign(density=lambda df: df.resource_count / df.area_km2)
        .sort_values("density", ascending=False)
    )

    density_df = density_df.rename(columns={"AREA_NAME": "neighbourhood"})

    return density_df
