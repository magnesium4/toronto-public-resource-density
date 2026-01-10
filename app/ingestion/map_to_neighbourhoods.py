import geopandas as gpd
from shapely.geometry import Point
import pandas as pd

from neighbourhoods import load_neighbourhoods_with_area
from load_washrooms import load_geojson, parse_features


def map_resources_to_neighbourhoods(resources_df, neighbourhoods_gdf):
    # Convert washrooms to GeoDataFrame
    geometry = [
        Point(lon, lat)
        for lon, lat in zip(resources_df["longitude"], resources_df["latitude"])
    ]

    washrooms_gdf = gpd.GeoDataFrame(
        resources_df.copy(),
        geometry=geometry,
        crs="EPSG:4326",  # lat/lon
    )

    # Reproject washrooms to match neighbourhood CRS
    washrooms_gdf = washrooms_gdf.to_crs(neighbourhoods_gdf.crs)

    # Spatial join
    joined = gpd.sjoin(
        washrooms_gdf,
        neighbourhoods_gdf,
        how="left",
        predicate="within",
    )

    return joined


def main():
    washrooms_df = parse_features(load_geojson())
    neighbourhoods_gdf = load_neighbourhoods_with_area()

    mapped_gdf = map_resources_to_neighbourhoods(
        washrooms_df, neighbourhoods_gdf
    )

    density = (
        mapped_gdf.groupby("AREA_NAME")
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

    print(density.head(10))


if __name__ == "__main__":
    main()
